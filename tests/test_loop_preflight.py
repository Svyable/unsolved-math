from datetime import UTC, datetime
from pathlib import Path

from oplab.launch import assess_loop_readiness, load_launch_card


def test_first_run_uses_pinned_provisional_without_inventing_rank(
    project_root: Path,
) -> None:
    report = assess_loop_readiness(
        project_root,
        as_of=datetime(2026, 8, 26, 0, 0, tzinfo=UTC),
    )

    assert report.ready is True
    assert report.selection_mode == "provisional_launch_card"
    assert report.selected_problem_id == "COMB-001"
    assert any("not a ranking" in warning for warning in report.warnings)


def test_expired_launch_card_blocks_unranked_reuse(project_root: Path) -> None:
    report = assess_loop_readiness(
        project_root,
        as_of=datetime(2026, 8, 28, 0, 0, tzinfo=UTC),
    )

    assert report.ready is False
    assert report.selection_mode == "blocked"
    assert any("expired" in blocker for blocker in report.blockers)


def test_launch_statement_and_sources_are_pinned(project_root: Path) -> None:
    card = load_launch_card(project_root / "config" / "first-run.json")
    candidate = card.candidates[0]

    assert len(candidate.upstream_revision) == 40
    assert len(candidate.source_urls) >= 2
    assert candidate.selection_basis == "PROVISIONAL_BOOTSTRAP_NOT_RANKED"
