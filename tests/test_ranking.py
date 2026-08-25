import json
from datetime import date
from pathlib import Path

from oplab.config import load_ranking_config
from oplab.normalization import normalize_problem
from oplab.ranking import build_queues


def test_research_and_review_queues_have_separate_guardrails(
    project_root: Path, fixture_path: Path
) -> None:
    config, _ = load_ranking_config(project_root / "config" / "ranking.toml")
    raw = json.loads(fixture_path.read_text(encoding="utf-8"))
    problems = [normalize_problem(record, config) for record in raw]

    research, status_review = build_queues(problems, config, as_of=date(2026, 8, 25), limit=100)
    research_ids = [item.problem_id for item in research]
    review_ids = [item.problem_id for item in status_review]

    assert research_ids == ["GOOD-001", "MED-002"]
    assert "HARD-003" not in research_ids
    assert "BAD-004" not in research_ids
    assert "SOLVED-005" not in research_ids
    assert "CONFLICT-006" not in research_ids
    assert review_ids[0] == "BAD-004"
    assert "CONFLICT-006" in review_ids
    assert all(item.components and item.reasons for item in research + status_review)
