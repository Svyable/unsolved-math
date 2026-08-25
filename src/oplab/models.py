from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ClaimTrust(StrEnum):
    UNVERIFIED_EXTERNAL_METADATA = "UNVERIFIED_EXTERNAL_METADATA"
    UNVERIFIED_OBSERVED_CHANGE = "UNVERIFIED_OBSERVED_CHANGE"


class NormalizedProblem(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    problem_id: str
    upstream_id: str | None = None
    title: str
    imported_status: str
    category: str | None = None
    difficulty_level: int | None = Field(default=None, ge=1, le=5)
    statement_status: str = "unknown"
    research_classification: str | None = None
    source_url: str | None = None
    source_citation: str | None = None
    upstream_updated_at: str | None = None
    literature_checked_at: str | None = None
    computational_keywords: tuple[str, ...] = ()
    suspicious_content: bool = False
    raw_record_sha256: str
    claim_trust: Literal[ClaimTrust.UNVERIFIED_EXTERNAL_METADATA] = (
        ClaimTrust.UNVERIFIED_EXTERNAL_METADATA
    )


class StatusChange(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    problem_id: str
    title: str
    previous_imported_status: str
    current_imported_status: str
    observed_at: datetime
    source_revision: str
    claim_trust: Literal[ClaimTrust.UNVERIFIED_OBSERVED_CHANGE] = (
        ClaimTrust.UNVERIFIED_OBSERVED_CHANGE
    )


class RankedProblem(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    problem_id: str
    title: str
    imported_status: str
    difficulty_level: int | None
    category: str | None
    score: float = Field(ge=0, le=100)
    components: dict[str, float]
    reasons: tuple[str, ...]
    claim_trust: Literal[ClaimTrust.UNVERIFIED_EXTERNAL_METADATA] = (
        ClaimTrust.UNVERIFIED_EXTERNAL_METADATA
    )


class SourceManifest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: int
    dataset_id: str
    source_filename: str
    requested_revision: str
    resolved_revision: str
    retrieved_at: datetime
    source_sha256: str
    ranking_config_sha256: str
    record_count: int = Field(ge=0)
    artifacts: dict[str, str]
    claim_trust: Literal[ClaimTrust.UNVERIFIED_EXTERNAL_METADATA] = (
        ClaimTrust.UNVERIFIED_EXTERNAL_METADATA
    )


class SyncOutcome(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    changed: bool
    resolved_revision: str
    record_count: int = 0
    added_count: int = 0
    removed_count: int = 0
    status_change_count: int = 0
    research_queue_count: int = 0
    status_review_queue_count: int = 0
    message: str


class ValidationReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    valid: bool
    checks: tuple[str, ...]
    errors: tuple[str, ...]
