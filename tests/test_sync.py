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
