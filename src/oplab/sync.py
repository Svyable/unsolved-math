from __future__ import annotations

import json
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any

import ijson
from pydantic import ValidationError

from oplab.artifacts import atomic_write_bytes, jsonl_bytes, model_jsonl_bytes, read_model_jsonl
from oplab.config import RankingConfig, load_ranking_config
from oplab.constants import SCHEMA_VERSION, UNVERIFIED_WARNING
from oplab.errors import IntegrityError, RecordValidationError
from oplab.hashing import canonical_json_bytes, sha256_bytes, sha256_file
from oplab.models import (
    NormalizedProblem,
    RankedProblem,
    SourceManifest,
    StatusChange,
    SyncOutcome,
)
from oplab.normalization import normalize_problem
from oplab.ranking import build_queues
from oplab.snapshots import SnapshotStore
from oplab.sources import ProblemSource


def _iter_records(path: Path) -> Iterator[Mapping[str, Any]]:
    try:
        with path.open("rb") as handle:
            for position, value in enumerate(ijson.items(handle, "item"), start=1):
                if not isinstance(value, Mapping):
                    raise RecordValidationError(f"record {position} is not a JSON object")
                yield value
    except (OSError, ijson.JSONError) as exc:
        raise RecordValidationError(f"cannot stream JSON array from {path}: {exc}") from exc


def _load_manifest(path: Path) -> SourceManifest | None:
    if not path.exists():
        return None
    try:
        return SourceManifest.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValidationError, ValueError) as exc:
        raise IntegrityError(f"invalid current manifest {path}: {exc}") from exc


def _queue_json_bytes(
    queue: list[RankedProblem], *, queue_name: str, generated_for: str, config_version: int
) -> bytes:
    return canonical_json_bytes(
        {
            "queue": queue_name,
            "generated_for_revision": generated_for,
            "ranking_config_version": config_version,
            "warning": UNVERIFIED_WARNING,
            "items": [item.model_dump(mode="json") for item in queue],
        }
    )


def _queue_markdown(queue: list[RankedProblem], *, title: str, generated_for: str) -> bytes:
    lines = [
        f"# {title}",
        "",
        f"> {UNVERIFIED_WARNING}",
        "",
        f"Upstream revision: `{generated_for}`",
        "",
        "| Rank | Score | Problem | Status | Difficulty | Category |",
        "|---:|---:|---|---|---:|---|",
    ]
    for rank, item in enumerate(queue, start=1):
        safe_title = item.title.replace("|", "\\|").replace("\n", " ")
        difficulty = f"L{item.difficulty_level}" if item.difficulty_level else "unknown"
        lines.append(
            f"| {rank} | {item.score:.2f} | `{item.problem_id}` — {safe_title} | "
            f"{item.imported_status} | {difficulty} | {item.category or 'unknown'} |"
        )
    lines.extend(
        [
            "",
            "Machine-readable score components and reasons are in the adjacent JSON file.",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def _summary_markdown(
    *,
    revision: str,
    record_count: int,
    added_count: int,
    removed_count: int,
    changes: list[StatusChange],
    research_count: int,
    review_count: int,
) -> bytes:
    lines = [
        "# Sync summary",
        "",
        f"> {UNVERIFIED_WARNING}",
        "",
        f"- Immutable upstream revision: `{revision}`",
        f"- Normalized records: {record_count}",
        f"- Added records: {added_count}",
        f"- Removed records: {removed_count}",
        f"- Imported status changes: {len(changes)}",
        f"- Research queue entries: {research_count}",
        f"- Status-review queue entries: {review_count}",
        "",
        "## Imported status changes",
        "",
    ]
    if not changes:
        lines.append("No imported status changes were observed relative to the tracked index.")
    else:
        lines.extend(["| Problem | Previous | Current |", "|---|---|---|"])
        for change in changes:
            safe_title = change.title.replace("|", "\\|").replace("\n", " ")
            lines.append(
                f"| `{change.problem_id}` — {safe_title} | "
                f"{change.previous_imported_status} | {change.current_imported_status} |"
            )
    lines.extend(
        [
            "",
            "These are changes in external metadata. They require independent review before any "
            "mathematical conclusion.",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


class SyncService:
    def __init__(
        self,
        *,
        repo_root: Path,
        source: ProblemSource,
        config_path: Path | None = None,
        snapshot_root: Path | None = None,
    ) -> None:
        self.repo_root = repo_root
        self.source = source
        self.config_path = config_path or repo_root / "config" / "ranking.toml"
        self.snapshot_store = SnapshotStore(snapshot_root or repo_root / ".oplab" / "snapshots")

    def run(self, *, force: bool = False, queue_limit: int = 200) -> SyncOutcome:
        artifact = self.source.fetch()
        source_sha = sha256_file(artifact.path)
        snapshot = self.snapshot_store.store(
            artifact.path,
            revision=artifact.resolved_revision,
            expected_sha256=source_sha,
        )
        config, config_sha = load_ranking_config(self.config_path)
        current_dir = self.repo_root / "data" / "current"
        manifest_path = current_dir / "manifest.json"
        current_manifest = _load_manifest(manifest_path)
        if (
            not force
            and current_manifest is not None
            and current_manifest.resolved_revision == artifact.resolved_revision
            and current_manifest.source_sha256 == source_sha
            and current_manifest.ranking_config_sha256 == config_sha
        ):
            return SyncOutcome(
                changed=False,
                resolved_revision=artifact.resolved_revision,
                record_count=current_manifest.record_count,
                message="upstream revision and ranking configuration are unchanged",
            )

        problems: list[NormalizedProblem] = []
        seen: set[str] = set()
        for position, raw in enumerate(_iter_records(snapshot), start=1):
            try:
                problem = normalize_problem(raw, config)
            except RecordValidationError as exc:
                raise RecordValidationError(
                    f"normalization failed at record {position}: {exc}"
                ) from exc
            if problem.problem_id in seen:
                raise RecordValidationError(f"duplicate canonical problem ID: {problem.problem_id}")
            seen.add(problem.problem_id)
            problems.append(problem)
        problems.sort(key=lambda item: item.problem_id)

        previous = {
            problem.problem_id: problem
            for problem in read_model_jsonl(current_dir / "problems.jsonl", NormalizedProblem)
        }
        current = {problem.problem_id: problem for problem in problems}
        added_count = len(current.keys() - previous.keys())
        removed_count = len(previous.keys() - current.keys())
        changes = [
            StatusChange(
                problem_id=problem_id,
                title=current[problem_id].title,
                previous_imported_status=previous[problem_id].imported_status,
                current_imported_status=current[problem_id].imported_status,
                observed_at=artifact.retrieved_at,
                source_revision=artifact.resolved_revision,
            )
            for problem_id in sorted(current.keys() & previous.keys())
            if previous[problem_id].imported_status != current[problem_id].imported_status
        ]

        research_queue, review_queue = build_queues(
            problems,
            config,
            as_of=artifact.retrieved_at.date(),
            limit=queue_limit,
        )
        outputs = self._build_outputs(
            problems=problems,
            config=config,
            revision=artifact.resolved_revision,
            changes=changes,
            added_count=added_count,
            removed_count=removed_count,
            research_queue=research_queue,
            review_queue=review_queue,
        )
        history_path = self.repo_root / "data" / "status-history.jsonl"
        history_bytes = self._merged_history(history_path, changes)
        outputs["data/status-history.jsonl"] = history_bytes

        for relative_path, content in outputs.items():
            atomic_write_bytes(self.repo_root / relative_path, content)

        artifact_hashes = {
            relative_path: sha256_bytes(content)
            for relative_path, content in sorted(outputs.items())
        }
        manifest = SourceManifest(
            schema_version=SCHEMA_VERSION,
            dataset_id=artifact.dataset_id,
            source_filename=artifact.source_filename,
            requested_revision=artifact.requested_revision,
            resolved_revision=artifact.resolved_revision,
            retrieved_at=artifact.retrieved_at,
            source_sha256=source_sha,
            ranking_config_sha256=config_sha,
            record_count=len(problems),
            artifacts=artifact_hashes,
        )
        atomic_write_bytes(manifest_path, canonical_json_bytes(manifest.model_dump(mode="json")))
        return SyncOutcome(
            changed=True,
            resolved_revision=artifact.resolved_revision,
            record_count=len(problems),
            added_count=added_count,
            removed_count=removed_count,
            status_change_count=len(changes),
            research_queue_count=len(research_queue),
            status_review_queue_count=len(review_queue),
            message="tracked artifacts rebuilt; imported claims remain unverified",
        )

    def _build_outputs(
        self,
        *,
        problems: list[NormalizedProblem],
        config: RankingConfig,
        revision: str,
        changes: list[StatusChange],
        added_count: int,
        removed_count: int,
        research_queue: list[RankedProblem],
        review_queue: list[RankedProblem],
    ) -> dict[str, bytes]:
        return {
            "data/current/problems.jsonl": model_jsonl_bytes(problems),
            "data/current/sync-summary.md": _summary_markdown(
                revision=revision,
                record_count=len(problems),
                added_count=added_count,
                removed_count=removed_count,
                changes=changes,
                research_count=len(research_queue),
                review_count=len(review_queue),
            ),
            "data/queues/research.json": _queue_json_bytes(
                research_queue,
                queue_name="research",
                generated_for=revision,
                config_version=config.version,
            ),
            "data/queues/research.md": _queue_markdown(
                research_queue,
                title="Research candidates",
                generated_for=revision,
            ),
            "data/queues/status-review.json": _queue_json_bytes(
                review_queue,
                queue_name="status-review",
                generated_for=revision,
                config_version=config.version,
            ),
            "data/queues/status-review.md": _queue_markdown(
                review_queue,
                title="Status-review candidates",
                generated_for=revision,
            ),
        }

    @staticmethod
    def _merged_history(path: Path, changes: list[StatusChange]) -> bytes:
        existing: list[dict[str, Any]] = []
        if path.exists():
            try:
                for line_number, line in enumerate(
                    path.read_text(encoding="utf-8").splitlines(), 1
                ):
                    if line.strip():
                        value = json.loads(line)
                        if not isinstance(value, dict):
                            raise IntegrityError(f"history line {line_number} is not a JSON object")
                        existing.append(value)
            except (OSError, json.JSONDecodeError) as exc:
                raise IntegrityError(f"invalid status history {path}: {exc}") from exc
        keys = {
            (
                item.get("problem_id"),
                item.get("source_revision"),
                item.get("previous_imported_status"),
                item.get("current_imported_status"),
            )
            for item in existing
        }
        for change in changes:
            key = (
                change.problem_id,
                change.source_revision,
                change.previous_imported_status,
                change.current_imported_status,
            )
            if key not in keys:
                existing.append(change.model_dump(mode="json"))
                keys.add(key)
        return jsonl_bytes(existing)
