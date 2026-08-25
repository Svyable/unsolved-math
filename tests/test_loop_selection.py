from datetime import UTC, datetime
from pathlib import Path

from oplab.loop import LoopHistoryEntry, select_next_candidate
from oplab.loop_config import load_research_loop_config
from oplab.models import RankedProblem
from oplab.research import ResearchConclusion


def _ranked(problem_id: str, score: float) -> RankedProblem:
    return RankedProblem(
        problem_id=problem_id,
        title=f"Candidate {problem_id}",
        imported_status="open",
        difficulty_level=2,
        category="combinatorics",
        score=score,
        components={"tractability": 1.0},
        reasons=("fixture",),
    )


def test_selection_respects_cooldown(project_root: Path) -> None:
    config, _ = load_research_loop_config(project_root / "config" / "research-loop.toml")
    now = datetime(2026, 8, 25, 23, 30, tzinfo=UTC)
    history = [
        LoopHistoryEntry(
            cycle_id="cycle-1",
            problem_id="TOP-001",
            completed_at=datetime(2026, 8, 25, 23, 0, tzinfo=UTC),
            material_progress=True,
            conclusion=ResearchConclusion.CONTINUE,
        )
    ]

    decision = select_next_candidate(
        [_ranked("TOP-001", 95), _ranked("NEXT-002", 90)],
        history,
        config,
        as_of=now,
    )

    assert decision.selected is not None
    assert decision.selected.problem_id == "NEXT-002"
