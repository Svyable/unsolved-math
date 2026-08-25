from __future__ import annotations

import os
import re
import shutil
import tempfile
from pathlib import Path

from oplab.errors import SnapshotConflictError
from oplab.hashing import sha256_file

SAFE_REVISION = re.compile(r"^[A-Za-z0-9._-]+$")


class SnapshotStore:
    def __init__(self, root: Path) -> None:
        self.root = root

    def store(self, source: Path, *, revision: str, expected_sha256: str) -> Path:
        if not SAFE_REVISION.fullmatch(revision):
            raise SnapshotConflictError(f"unsafe snapshot revision: {revision!r}")
        destination_dir = self.root / revision
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination = destination_dir / "problems.json"

        if destination.exists():
            existing_sha = sha256_file(destination)
            if existing_sha != expected_sha256:
                raise SnapshotConflictError(
                    f"immutable snapshot conflict at {destination}: "
                    f"expected {expected_sha256}, found {existing_sha}"
                )
            return destination

        with tempfile.NamedTemporaryFile(dir=destination_dir, delete=False) as temporary:
            temporary_path = Path(temporary.name)
            with source.open("rb") as source_handle:
                shutil.copyfileobj(source_handle, temporary)
            temporary.flush()
            os.fsync(temporary.fileno())

        try:
            actual_sha = sha256_file(temporary_path)
            if actual_sha != expected_sha256:
                raise SnapshotConflictError(
                    f"copied snapshot hash mismatch: expected {expected_sha256}, found {actual_sha}"
                )
            try:
                os.link(temporary_path, destination)
            except FileExistsError as exc:
                existing_sha = sha256_file(destination)
                if existing_sha != expected_sha256:
                    raise SnapshotConflictError(
                        f"concurrent immutable snapshot conflict at {destination}"
                    ) from exc
        finally:
            temporary_path.unlink(missing_ok=True)
        return destination
