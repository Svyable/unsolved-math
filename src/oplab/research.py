from __future__ import annotations

import re
from datetime import datetime
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
AUTONOMOUS_SOLVE_CLAIM = re.compile(
    r"\b(?:the\s+)?(?:problem|conjecture)\s+(?:is\s+)?(?:solved|proved|resolved)\b",
    re.IGNORECASE,
)


class ClaimStatus(StrEnum):
    UNVERIFIED = "UNVERIFIED"
    HYPOTHESIS = "HYPOTHESIS"
    FALSIFIED = "FALSIFIED"
    EXPERIMENTALLY_SUPPORTED = "EXPERIMENTALLY_SUPPORTED"
    PRIMARY_SOURCE_SUPPORTED = "PRIMARY_SOURCE_SUPPORTED"
    FORMALLY_VERIFIED_SUBLEMMA = "FORMALLY_VERIFIED_SUBLEMMA"


class ProgressKind(StrEnum):
    NEW_FALSIFIABLE_HYPOTHESIS = "NEW_FALSIFIABLE_HYPOTHESIS"
    ASSUMPTION_REDUCTION = "ASSUMPTION_REDUCTION"
    EQUIVALENT_REFORMULATION = "EQUIVALENT_REFORMULATION"
    REPRODUCIBLE_EXPERIMENT = "REPRODUCIBLE_EXPERIMENT"
    COUNTEREXAMPLE = "COUNTEREXAMPLE"
    PRIMARY_SOURCE_VERIFICATION = "PRIMARY_SOURCE_VERIFICATION"
    PROOF_GAP_IDENTIFIED = "PROOF_GAP_IDENTIFIED"
    APPROACH_RETIRED = "APPROACH_RETIRED"
    FORMALLY_VERIFIED_SUBLEMMA = "FORMALLY_VERIFIED_SUBLEMMA"
    INFRASTRUCTURE_ENABLER = "INFRASTRUCTURE_ENABLER"


class ResearchConclusion(StrEnum):
    CONTINUE = "CONTINUE"
    BLOCKED = "BLOCKED"
    FALSIFIED_SUBCLAIM = "FALSIFIED_SUBCLAIM"
    FORMALLY_VERIFIED_SUBLEMMA = "FORMALLY_VERIFIED_SUBLEMMA"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"


class ArtifactRef(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    path: str = Field(min_length=1, max_length=512)
    sha256: str
    media_type: str = Field(min_length=1, max_length=128)

    @field_validator("path")
    @classmethod
    def path_is_cycle_relative(cls, value: str) -> str:
        parsed = PurePosixPath(value)
        if parsed.is_absolute() or ".." in parsed.parts or "\\" in value:
            raise ValueError(
                "artifact paths must be safe POSIX paths relative to the cycle directory"
            )
        return value

    @field_validator("sha256")
    @classmethod
    def sha_is_valid(cls, value: str) -> str:
        if not SHA256_PATTERN.fullmatch(value):
            raise ValueError("sha256 must be a lowercase 64-character digest")
        return value


class ResearchClaim(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    claim_id: str
    statement: str = Field(min_length=1)
    status: ClaimStatus
    dependencies: tuple[str, ...] = ()

    @field_validator("claim_id")
    @classmethod
    def claim_id_is_valid(cls, value: str) -> str:
        if not ID_PATTERN.fullmatch(value):
            raise ValueError("claim_id contains unsupported characters")
        return value


class ProgressUnit(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    unit_id: str
    kind: ProgressKind
    summary: str = Field(min_length=1)
    claim_ids: tuple[str, ...] = Field(min_length=1)
    evidence: tuple[ArtifactRef, ...] = Field(min_length=1)

    @field_validator("unit_id")
    @classmethod
    def unit_id_is_valid(cls, value: str) -> str:
        if not ID_PATTERN.fullmatch(value):
            raise ValueError("unit_id contains unsupported characters")
        return value


class TheoryLane(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    target: str = Field(min_length=1)
    definitions: tuple[str, ...] = Field(min_length=1)
    assumptions: tuple[str, ...]
    approaches_considered: tuple[str, ...] = Field(min_length=2)
    falsification_targets: tuple[str, ...] = Field(min_length=1)
    claims: tuple[ResearchClaim, ...] = Field(min_length=1)
    progress: tuple[ProgressUnit, ...] = Field(min_length=1)


class VerificationCheck(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    check_id: str
    claim_ids: tuple[str, ...] = Field(min_length=1)
    method: str = Field(min_length=1)
    independent_context: Literal[True]
    result: str = Field(min_length=1)
    reproduction_command: str | None = None
    evidence: tuple[ArtifactRef, ...] = Field(min_length=1)
    blocking_objections: tuple[str, ...] = ()

    @field_validator("check_id")
    @classmethod
    def check_id_is_valid(cls, value: str) -> str:
        if not ID_PATTERN.fullmatch(value):
            raise ValueError("check_id contains unsupported characters")
        return value


class VerificationLane(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    checks: tuple[VerificationCheck, ...] = Field(min_length=1)
    progress: tuple[ProgressUnit, ...] = Field(min_length=1)
    unresolved_objections: tuple[str, ...] = ()


class ResearchCycle(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal[1] = 1
    cycle_id: str
    problem_id: str
    upstream_snapshot_revision: str = Field(min_length=1)
    parent_cycle_id: str | None = None
    started_at: datetime
    completed_at: datetime
    selection_basis: str = Field(min_length=1)
    theory: TheoryLane
    verification: VerificationLane
    material_progress: Literal[True] = True
    conclusion: ResearchConclusion
    next_step: str = Field(min_length=1)

    @field_validator("cycle_id", "problem_id")
    @classmethod
    def identifiers_are_valid(cls, value: str) -> str:
        if not ID_PATTERN.fullmatch(value):
            raise ValueError("identifier contains unsupported characters")
        return value

    @model_validator(mode="after")
    def cross_lane_contract_holds(self) -> Self:
        if self.completed_at < self.started_at:
            raise ValueError("completed_at cannot precede started_at")
        claim_ids = [claim.claim_id for claim in self.theory.claims]
        if len(claim_ids) != len(set(claim_ids)):
            raise ValueError("theory claim IDs must be unique")
        known = set(claim_ids)
        referenced = {
            claim_id
            for progress in (*self.theory.progress, *self.verification.progress)
            for claim_id in progress.claim_ids
        }
        referenced.update(
            claim_id for check in self.verification.checks for claim_id in check.claim_ids
        )
        unknown = referenced - known
        if unknown:
            raise ValueError(
                f"verification/progress references unknown claim IDs: {sorted(unknown)}"
            )
        if self.conclusion == ResearchConclusion.FORMALLY_VERIFIED_SUBLEMMA and not any(
            claim.status == ClaimStatus.FORMALLY_VERIFIED_SUBLEMMA for claim in self.theory.claims
        ):
            raise ValueError("formalized conclusion requires a formally verified claim")
        prose = "\n".join(
            [
                self.selection_basis,
                self.theory.target,
                *(claim.statement for claim in self.theory.claims),
                *(unit.summary for unit in self.theory.progress),
                *(check.result for check in self.verification.checks),
                *(unit.summary for unit in self.verification.progress),
                self.next_step,
            ]
        )
        if AUTONOMOUS_SOLVE_CLAIM.search(prose):
            raise ValueError("autonomous parent-problem solve claims are forbidden")
        return self

    def artifact_refs(self) -> tuple[ArtifactRef, ...]:
        refs = [artifact for unit in self.theory.progress for artifact in unit.evidence]
        refs.extend(artifact for check in self.verification.checks for artifact in check.evidence)
        refs.extend(artifact for unit in self.verification.progress for artifact in unit.evidence)
        unique: dict[tuple[str, str], ArtifactRef] = {
            (artifact.path, artifact.sha256): artifact for artifact in refs
        }
        return tuple(unique.values())
