import json
from datetime import UTC, datetime
from pathlib import Path

from oplab.dashboard import render_readme_dashboard
from oplab.loop import LoopHistoryEntry
from oplab.models import RankedProblem
from oplab.research import ResearchConclusion


def _ranked(problem_id: str, title: str, score: float) -> RankedProblem:
    return RankedProblem(
        problem_id=problem_id,
        title=title,
        imported_status="open",
        difficulty_level=2,
        category="combinatorics",
        score=score,
        components={"tractability": 1.0},
        reasons=("fixture",),
    )


def test_dashboard_shows_provisional_stack_without_calling_it_ranked(
    project_root: Path,
) -> None:
    rendered = render_readme_dashboard(project_root, as_of=datetime(2026, 8, 27, 1, 49, tzinfo=UTC))

    assert "Current research stack" in rendered
    assert "COMB-001 — The Hadwiger-Nelson Problem" in rendered
    assert "| 1 | — | `COMB-001" in rendered
    assert "| 2 | `CONTINUE`" in rendered
    assert "provisional activity order, not a ranking" in rendered
    assert "no provisional candidate passed cooldown and anti-thrashing gates" in rendered


def test_dashboard_preserves_queue_rank_after_gates(tmp_path: Path, project_root: Path) -> None:
    (tmp_path / "config").mkdir()
    (tmp_path / "data" / "queues").mkdir(parents=True)
    (tmp_path / "data" / "research-loop").mkdir(parents=True)
    (tmp_path / "config" / "research-loop.toml").write_bytes(
        (project_root / "config" / "research-loop.toml").read_bytes()
    )
    history = LoopHistoryEntry(
        cycle_id="cycle-top",
        problem_id="TOP-001",
        completed_at=datetime(2026, 8, 27, 1, 30, tzinfo=UTC),
        material_progress=True,
        conclusion=ResearchConclusion.CONTINUE,
    )
    (tmp_path / "data" / "research-loop" / "history.jsonl").write_text(
        history.model_dump_json() + "\n", encoding="utf-8"
    )
    queue = [_ranked("TOP-001", "Top candidate", 95), _ranked("NEXT-002", "Next", 90)]
    (tmp_path / "data" / "queues" / "research.json").write_text(
        json.dumps({"items": [item.model_dump(mode="json") for item in queue]}),
        encoding="utf-8",
    )

    rendered = render_readme_dashboard(tmp_path, as_of=datetime(2026, 8, 27, 2, 0, tzinfo=UTC))

    assert "| 1 | 1 | `TOP-001 — TOP-001` | 1 | `CONTINUE`" in rendered
    assert "| 1 | 2 | `NEXT-002 — Next` | 90.00" in rendered
    assert "| 1 | 1 | `TOP-001 — Top candidate` | 95.00" not in rendered
