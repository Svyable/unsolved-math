from pathlib import Path

import pytest

from oplab.errors import SnapshotConflictError
from oplab.hashing import sha256_file
from oplab.snapshots import SnapshotStore


def test_snapshot_is_immutable(tmp_path: Path, fixture_path: Path) -> None:
    store = SnapshotStore(tmp_path / "snapshots")
    source_hash = sha256_file(fixture_path)
    stored = store.store(fixture_path, revision="abc123", expected_sha256=source_hash)

    stored.write_text("[]", encoding="utf-8")

    with pytest.raises(SnapshotConflictError):
        store.store(fixture_path, revision="abc123", expected_sha256=source_hash)
