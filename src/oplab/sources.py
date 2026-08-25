from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from huggingface_hub import HfApi, hf_hub_download

from oplab.constants import DATASET_ID, SOURCE_FILENAME
from oplab.errors import NetworkPermissionError, OplabError
from oplab.hashing import sha256_file


@dataclass(frozen=True)
class SourceArtifact:
    path: Path
    dataset_id: str
    source_filename: str
    requested_revision: str
    resolved_revision: str
    retrieved_at: datetime


class ProblemSource(Protocol):
    def fetch(self) -> SourceArtifact: ...


@dataclass(frozen=True)
class HuggingFaceSource:
    revision: str = "main"
    allow_network: bool = False
    dataset_id: str = DATASET_ID

    def fetch(self) -> SourceArtifact:
        if not self.allow_network:
            raise NetworkPermissionError(
                "network sync is disabled; pass --allow-network or use --local-path"
            )
        try:
            info = HfApi().dataset_info(repo_id=self.dataset_id, revision=self.revision)
        except (ImportError, OSError, ValueError) as exc:
            raise OplabError(
                f"failed to resolve Hugging Face revision {self.revision}: {exc}"
            ) from exc
        if not info.sha:
            raise OplabError(f"Hugging Face returned no commit SHA for {self.revision}")
        try:
            downloaded = hf_hub_download(
                repo_id=self.dataset_id,
                filename=SOURCE_FILENAME,
                revision=info.sha,
                repo_type="dataset",
            )
        except (ImportError, OSError, ValueError) as exc:
            raise OplabError(f"failed to download {SOURCE_FILENAME} at {info.sha}: {exc}") from exc
        return SourceArtifact(
            path=Path(downloaded),
            dataset_id=self.dataset_id,
            source_filename=SOURCE_FILENAME,
            requested_revision=self.revision,
            resolved_revision=info.sha,
            retrieved_at=datetime.now(UTC),
        )


@dataclass(frozen=True)
class LocalJsonSource:
    path: Path
    source_revision: str | None = None
    dataset_id: str = DATASET_ID

    def fetch(self) -> SourceArtifact:
        if not self.path.is_file():
            raise OplabError(f"local source does not exist or is not a file: {self.path}")
        source_sha = sha256_file(self.path)
        resolved = self.source_revision or f"local-{source_sha}"
        return SourceArtifact(
            path=self.path,
            dataset_id=self.dataset_id,
            source_filename=self.path.name,
            requested_revision=self.source_revision or resolved,
            resolved_revision=resolved,
            retrieved_at=datetime.now(UTC),
        )
