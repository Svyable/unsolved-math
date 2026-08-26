from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Literal, Self
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from oplab.artifacts import read_model_jsonl
from oplab.errors import IntegrityError, OplabError
from oplab.hashing import sha256_bytes
from oplab.loop import LoopHistoryEntry, load_ranked_queue, select_next_candidate
from oplab.loop_config import load_research_loop_config
from oplab.models import ClaimTrust

PROVISIONAL_SELECTION: Literal["PROVISIONAL_BOOTSTRAP_NOT_RANKED"] = (
    "PROVISIONAL_BOOTSTRAP_NOT_RANKED"
)


class LaunchCandidate(BaseModel):
    """Pinned, short-lived fallback used only before the ranked queue exists."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    problem_id: str = Field(min_length=1, max_length=128)
    title: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    statement_sha256: str
    imported_status: Literal["open", "partially_solved"]
    difficulty_level: int = Field(ge=1, le=3)
    category: str = Field(min_length=1)
    selection_basis: Literal["PROVISIONAL_BOOTSTRAP_NOT_RANKED"] = PROVISIONAL_SELECTION
    upstream_dataset: Literal["ulamai/UnsolvedMath"] = "ulamai/UnsolvedMath"
    upstream_revision: str
    upstream_file_sha256: str
    observed_at: datetime
    source_urls: tuple[str, ...] = Field(min_length=2)
    bounded_target: str = Field(min_length=1)
    theory_starting_points: tuple[str, ...] = Field(min_length=2)
    falsification_targets: tuple[str, ...] = Field(min_length=1)
    baseline_verification: str = Field(min_length=1)
    novelty_boundary: str = Field(min_length=1)
    claim_trust: Literal[ClaimTrust.UNVERIFIED_EXTERNAL_METADATA] = (
        ClaimTrust.UNVERIFIED_EXTERNAL_METADATA
    )

    @field_validator("statement_sha256", "upstream_file_sha256")
    @classmethod
    def digest_is_sha256(cls, value: str) -> str:
        if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
            raise ValueError("digest must be a lowercase SHA-256 value")
        return value

    @field_validator("upstream_revision")
    @classmethod
    def revision_is_immutable(cls, value: str) -> str:
        if len(value) != 40 or any(character not in "0123456789abcdef" for character in value):
            raise ValueError("upstream_revision must be a full 40-character commit SHA")
        return value

    @field_validator("observed_at")
    @classmethod
    def observation_is_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("observed_at must include a timezone")
        return value

    @field_validator("source_urls")
    @classmethod
    def sources_are_unique_https_urls(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("source URLs must be unique")
        for url in value:
            parsed = urlsplit(url)
            if parsed.scheme != "https" or not parsed.netloc:
                raise ValueError("source URLs must be absolute HTTPS URLs")
        return value

    @model_validator(mode="after")
    def statement_hash_matches(self) -> Self:
        actual = sha256_bytes(self.statement.encode("utf-8"))
        if actual != self.statement_sha256:
            raise ValueError("statement_sha256 does not match the frozen statement")
        return self


class FirstRunLaunchCard(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal[1] = 1
    generated_at: datetime
    expires_at: datetime
    purpose: str = Field(min_length=1)
    candidates: tuple[LaunchCandidate, ...] = Field(min_length=1)

    @field_validator("generated_at", "expires_at")
    @classmethod
    def timestamps_are_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("launch-card timestamps must include a timezone")
        return value

    @model_validator(mode="after")
    def validity_window_and_ids_are_sound(self) -> Self:
        if self.expires_at <= self.generated_at:
            raise ValueError("expires_at must follow generated_at")
        ids = [candidate.problem_id for candidate in self.candidates]
        if len(ids) != len(set(ids)):
            raise ValueError("launch-card problem IDs must be unique")
        return self


class LoopPreflightReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    ready: bool
    selection_mode: Literal["ranked_queue", "provisional_launch_card", "blocked"]
    selected_problem_id: str | None = None
    checks: tuple[str, ...]
    warnings: tuple[str, ...]
    blockers: tuple[str, ...]


def load_launch_card(path: Path) -> FirstRunLaunchCard:
    try:
        return FirstRunLaunchCard.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValidationError, ValueError) as exc:
        raise IntegrityError(f"invalid first-run launch card {path}: {exc}") from exc


def _provisional_candidate_outside_cooldown(
    card: FirstRunLaunchCard,
    history: list[LoopHistoryEntry],
    *,
    as_of: datetime,
    cooldown_hours: int,
    max_consecutive: int,
) -> LaunchCandidate | None:
    recent_cutoff = as_of - timedelta(hours=cooldown_hours)
    visible_history = [entry for entry in history if entry.completed_at <= as_of]
    recent_problem_ids = {
        entry.problem_id
        for entry in visible_history
        if entry.completed_at > recent_cutoff
    }
    ordered_history = sorted(
        visible_history, key=lambda entry: entry.completed_at, reverse=True
    )
    consecutive_id = ordered_history[0].problem_id if ordered_history else None
    consecutive_count = 0
    for entry in ordered_history:
        if entry.problem_id != consecutive_id:
            break
        consecutive_count += 1
    for candidate in card.candidates:
        if candidate.problem_id in recent_problem_ids:
            continue
        if candidate.problem_id == consecutive_id and consecutive_count >= max_consecutive:
            continue
        return candidate
    return None


def assess_loop_readiness(
    repo_root: Path, *, as_of: datetime | None = None
) -> LoopPreflightReport:
    """Resolve the first usable selection path without manufacturing a ranking."""

    now = as_of or datetime.now(UTC)
    if now.tzinfo is None:
        now = now.replace(tzinfo=UTC)
    checks: list[str] = []
    warnings: list[str] = []
    blockers: list[str] = []

    required_paths = (
        "AGENTS.md",
        "README.md",
        "docs/hourly-loop.md",
        "docs/research-integrity.md",
        "prompts/hourly-research-loop.md",
        "config/research-loop.toml",
    )
    for relative in required_paths:
        if not (repo_root / relative).is_file():
            blockers.append(f"missing required loop input: {relative}")
    if not blockers:
        checks.append("durable instructions and safety boundaries are present")

    try:
        config, _ = load_research_loop_config(repo_root / "config" / "research-loop.toml")
    except OplabError as exc:
        blockers.append(str(exc))
        return LoopPreflightReport(
            ready=False,
            selection_mode="blocked",
            checks=tuple(checks),
            warnings=tuple(warnings),
            blockers=tuple(blockers),
        )

    history = read_model_jsonl(
        repo_root / "data" / "research-loop" / "history.jsonl", LoopHistoryEntry
    )
    queue_path = repo_root / "data" / "queues" / "research.json"
    if queue_path.is_file():
        try:
            queue = load_ranked_queue(queue_path)
            decision = select_next_candidate(queue, history, config, as_of=now)
        except IntegrityError as exc:
            warnings.append(str(exc))
        else:
            if decision.selected is not None:
                checks.append("ranked queue has an eligible candidate outside loop gates")
                return LoopPreflightReport(
                    ready=not blockers,
                    selection_mode="ranked_queue" if not blockers else "blocked",
                    selected_problem_id=decision.selected.problem_id if not blockers else None,
                    checks=tuple(checks),
                    warnings=tuple(warnings),
                    blockers=tuple(blockers),
                )
            blockers.append(decision.reason)
            return LoopPreflightReport(
                ready=False,
                selection_mode="blocked",
                checks=tuple(checks),
                warnings=tuple(warnings),
                blockers=tuple(blockers),
            )
    else:
        warnings.append("ranked queue is absent; provisional fallback is not a ranking")

    manifest_path = repo_root / "data" / "current" / "manifest.json"
    if not manifest_path.is_file():
        warnings.append("tracked dataset manifest is absent; use only the pinned launch snapshot")

    try:
        card = load_launch_card(repo_root / "config" / "first-run.json")
    except IntegrityError as exc:
        blockers.append(str(exc))
    else:
        if now > card.expires_at:
            blockers.append("first-run launch card has expired and must be re-verified")
        else:
            candidate = _provisional_candidate_outside_cooldown(
                card,
                history,
                as_of=now,
                cooldown_hours=config.selection.cooldown_hours,
                max_consecutive=config.selection.max_consecutive_cycles_per_problem,
            )
            if candidate is None:
                blockers.append("no provisional candidate passed cooldown and anti-thrashing gates")
            elif not blockers:
                checks.append(
                    "short-lived pinned fallback has primary sources and a bounded target"
                )
                return LoopPreflightReport(
                    ready=True,
                    selection_mode="provisional_launch_card",
                    selected_problem_id=candidate.problem_id,
                    checks=tuple(checks),
                    warnings=tuple(warnings),
                    blockers=(),
                )

    return LoopPreflightReport(
        ready=False,
        selection_mode="blocked",
        checks=tuple(checks),
        warnings=tuple(warnings),
        blockers=tuple(blockers),
    )
