from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from oplab.artifacts import atomic_write_bytes, model_jsonl_bytes, read_model_jsonl
from oplab.cycle_store import load_cycle
from oplab.errors import IntegrityError
from oplab.loop_config import ResearchLoopConfig
from oplab.models import RankedProblem
from oplab.research import ResearchConclusion


class LoopHistoryEntry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    cycle_id: str
    problem_id: str
    completed_at: datetime
    material_progress: Literal[True]
    conclusion: ResearchConclusion

    @field_validator("completed_at")
    @classmethod
    def completion_time_is_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("completed_at must include a timezone")
        return value


class SelectionDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    selected: RankedProblem | None
    reason: str
    considered: int = Field(ge=0)


def load_ranked_queue(path: Path) -> list[RankedProblem]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        items = payload.get("items") if isinstance(payload, dict) else None
        if not isinstance(items, list):
            raise IntegrityError(f"queue has no items array: {path}")
        return [RankedProblem.model_validate(item) for item in items]
    except (OSError, json.JSONDecodeError, ValidationError, ValueError) as exc:
        raise IntegrityError(f"invalid ranked queue {path}: {exc}") from exc


def select_next_candidate(
    queue: list[RankedProblem],
    history: list[LoopHistoryEntry],
    config: ResearchLoopConfig,
    *,
    as_of: datetime | None = None,
) -> SelectionDecision:
    now = as_of or datetime.now(UTC)
    candidates = queue[: config.selection.top_k]
    recent_cutoff = now - timedelta(hours=config.selection.cooldown_hours)
    visible_history = [entry for entry in history if entry.completed_at <= now]
    last_by_problem: dict[str, datetime] = {}
    for entry in visible_history:
        previous = last_by_problem.get(entry.problem_id)
        if previous is None or entry.completed_at > previous:
            last_by_problem[entry.problem_id] = entry.completed_at

    consecutive_problem: str | None = None
    consecutive_count = 0
    for entry in sorted(
        visible_history, key=lambda value: value.completed_at, reverse=True
    ):
        if consecutive_problem is None:
            consecutive_problem = entry.problem_id
            consecutive_count = 1
        elif entry.problem_id == consecutive_problem:
            consecutive_count += 1
        else:
            break

    for candidate in candidates:
        last = last_by_problem.get(candidate.problem_id)
        if last is not None and last > recent_cutoff:
            continue
        if (
            candidate.problem_id == consecutive_problem
            and consecutive_count >= config.selection.max_consecutive_cycles_per_problem
        ):
            continue
        return SelectionDecision(
            selected=candidate,
            reason="highest-ranked candidate outside cooldown and anti-thrashing gates",
            considered=len(candidates),
        )
    return SelectionDecision(
        selected=None,
        reason="no ranked candidate passed cooldown and anti-thrashing gates",
        considered=len(candidates),
    )


def append_cycle_history(history_path: Path, cycle_dir: Path) -> LoopHistoryEntry:
    cycle = load_cycle(cycle_dir)
    entry = LoopHistoryEntry(
        cycle_id=cycle.cycle_id,
        problem_id=cycle.problem_id,
        completed_at=cycle.completed_at,
        material_progress=cycle.material_progress,
        conclusion=cycle.conclusion,
    )
    existing = read_model_jsonl(history_path, LoopHistoryEntry)
    if any(item.cycle_id == entry.cycle_id for item in existing):
        return entry
    existing.append(entry)
    existing.sort(key=lambda value: (value.completed_at, value.cycle_id))
    atomic_write_bytes(history_path, model_jsonl_bytes(existing))
    return entry
