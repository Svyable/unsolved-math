import json
import shutil
from pathlib import Path

from oplab.models import ClaimTrust
from oplab.sources import LocalJsonSource
from oplab.sync import SyncService
from oplab.validation import validate_repository


def _prepare_repo(tmp_path: Path, project_root: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    shutil.copy2(project_root / "config" / "ranking.toml", config_dir / "ranking.toml")


def test_sync_is_idempotent_and_status_changes_stay_unverified(
    tmp_path: Path, project_root: Path, fixture_path: Path
) -> None:
    _prepare_repo(tmp_path, project_root)
    service = SyncService(
        repo_root=tmp_path,
        source=LocalJsonSource(fixture_path, source_revision="fixture-v1"),
    )

    first = service.run(queue_limit=50)
    second = service.run(queue_limit=50)

    assert first.changed is True
    assert first.record_count == 6
    assert second.changed is False
    assert validate_repository(tmp_path).valid is True

    changed_path = tmp_path / "changed.json"
    records = json.loads(fixture_path.read_text(encoding="utf-8"))
    records[0]["status"] = "solved"
    changed_path.write_text(json.dumps(records), encoding="utf-8")
    changed_service = SyncService(
        repo_root=tmp_path,
        source=LocalJsonSource(changed_path, source_revision="fixture-v2"),
    )

    outcome = changed_service.run(queue_limit=50)
    history = [
        json.loads(line)
        for line in (tmp_path / "data" / "status-history.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line
    ]

    assert outcome.status_change_count == 1
    assert history[-1]["problem_id"] == "GOOD-001"
    assert history[-1]["claim_trust"] == ClaimTrust.UNVERIFIED_OBSERVED_CHANGE
    assert "verified" not in history[-1]
    assert validate_repository(tmp_path).valid is True


def test_sync_disambiguates_reused_problem_numbers_stably(
    tmp_path: Path, project_root: Path, fixture_path: Path
) -> None:
    repo_root = tmp_path / "collision-repo"
    repo_root.mkdir()
    _prepare_repo(repo_root, project_root)
    records = json.loads(fixture_path.read_text(encoding="utf-8"))[:2]
    records[1]["problem_number"] = records[0]["problem_number"]
    collision_path = tmp_path / "collisions.json"
    collision_path.write_text(json.dumps(records), encoding="utf-8")

    first = SyncService(
        repo_root=repo_root,
        source=LocalJsonSource(collision_path, source_revision="collision-v1"),
    ).run()
    first_index = [
        json.loads(line)
        for line in (repo_root / "data" / "current" / "problems.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]

    reversed_path = tmp_path / "collisions-reversed.json"
    reversed_path.write_text(json.dumps(list(reversed(records))), encoding="utf-8")
    second = SyncService(
        repo_root=repo_root,
        source=LocalJsonSource(reversed_path, source_revision="collision-v2"),
    ).run()
    second_index = [
        json.loads(line)
        for line in (repo_root / "data" / "current" / "problems.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]

    assert first.record_count == 2
    assert second.record_count == 2
    assert [(item["upstream_id"], item["problem_id"]) for item in first_index] == [
        ("1", "GOOD-001"),
        ("2", "GOOD-001--2"),
    ]
    assert second_index == first_index


def test_sync_refreshes_readme_ranked_next_up(
    tmp_path: Path, project_root: Path, fixture_path: Path
) -> None:
    _prepare_repo(tmp_path, project_root)
    shutil.copy2(
        project_root / "config" / "research-loop.toml",
        tmp_path / "config" / "research-loop.toml",
    )
    (tmp_path / "README.md").write_text(
        "# Fixture\n\n<!-- OPLAB:RESEARCH-STACK:START -->\nold\n"
        "<!-- OPLAB:RESEARCH-STACK:END -->\n",
        encoding="utf-8",
    )

    SyncService(
        repo_root=tmp_path,
        source=LocalJsonSource(fixture_path, source_revision="fixture-readme"),
    ).run(queue_limit=50)

    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "### Next up" in readme
    assert "Candidates retain their deterministic queue rank" in readme
    assert "`GOOD-001 — Finite graph coloring certificate`" in readme
    assert "PROVISIONAL_BOOTSTRAP_NOT_RANKED" not in readme
