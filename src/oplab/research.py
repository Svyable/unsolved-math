from __future__ import annotations

import re
from datetime import datetime
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Literal, Self
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from oplab.hashing import sha256_bytes
from oplab.models import ClaimTrust

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


class ClaimOrigin(StrEnum):
    IMPORTED_UNVERIFIED = "IMPORTED_UNVERIFIED"
    PRIMARY_SOURCE = "PRIMARY_SOURCE"
    DERIVED = "DERIVED"
    NOVEL_HYPOTHESIS = "NOVEL_HYPOTHESIS"


class VerificationMethod(StrEnum):
    COUNTEREXAMPLE_SEARCH = "COUNTEREXAMPLE_SEARCH"
    INDEPENDENT_IMPLEMENTATION = "INDEPENDENT_IMPLEMENTATION"
    PRIMARY_SOURCE_AUDIT = "PRIMARY_SOURCE_AUDIT"
    PROOF_STEP_AUDIT = "PROOF_STEP_AUDIT"
    FORMAL_KERNEL = "FORMAL_KERNEL"


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


class FrozenProblemSnapshot(BaseModel):
    """Exact problem input used by a cycle; imported fields remain claims."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    snapshot_schema_version: Literal[1] = 1
    problem_id: str
    title: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    statement_sha256: str
    upstream_dataset: str = Field(min_length=1)
    upstream_revision: str = Field(min_length=1)
    upstream_file_sha256: str
    frozen_at: datetime
    source_urls: tuple[str, ...] = Field(min_length=2)
    imported_status: str = Field(min_length=1)
    selection_basis: str = Field(min_length=1)
    claim_trust: Literal[ClaimTrust.UNVERIFIED_EXTERNAL_METADATA] = (
        ClaimTrust.UNVERIFIED_EXTERNAL_METADATA
    )

    @field_validator("problem_id")
    @classmethod
    def problem_identifier_is_valid(cls, value: str) -> str:
        if not ID_PATTERN.fullmatch(value):
            raise ValueError("problem_id contains unsupported characters")
        return value

    @field_validator("statement_sha256", "upstream_file_sha256")
    @classmethod
    def digest_is_valid(cls, value: str) -> str:
        if not SHA256_PATTERN.fullmatch(value):
            raise ValueError("digest must be a lowercase 64-character SHA-256 value")
        return value

    @field_validator("frozen_at")
    @classmethod
    def frozen_time_is_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("frozen_at must include a timezone")
        return value

    @field_validator("source_urls")
    @classmethod
    def sources_are_unique_https_urls(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("source URLs must be unique")
        for url in value:
            parsed = urlsplit(url)
            if parsed.scheme != "https" or not parsed.netloc:
                raise ValueError("source URLs must be absolute HTTPS URLs")
        return value

    @model_validator(mode="after")
    def statement_digest_matches(self) -> Self:
        actual = sha256_bytes(self.statement.encode("utf-8"))
        if actual != self.statement_sha256:
            raise ValueError("statement_sha256 does not match the frozen statement")
        return self

class ResearchClaim(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    claim_id: str
    statement: str = Field(min_length=1)
    status: ClaimStatus
    origin: ClaimOrigin
    falsification_condition: str = Field(min_length=1)
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
    method_family: VerificationMethod
    method: str = Field(min_length=1)
    independent_context: Literal[True]
    independence_basis: str = Field(min_length=1)
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

    schema_version: Literal[2] = 2
    cycle_id: str
    problem_id: str
    frozen_problem: FrozenProblemSnapshot
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
        if self.started_at.tzinfo is None or self.completed_at.tzinfo is None:
            raise ValueError("cycle timestamps must include a timezone")
        if self.problem_id != self.frozen_problem.problem_id:
            raise ValueError("cycle problem_id must match the frozen problem snapshot")
        claim_ids = [claim.claim_id for claim in self.theory.claims]
        if len(claim_ids) != len(set(claim_ids)):
            raise ValueError("theory claim IDs must be unique")
        known = set(claim_ids)
        for claim in self.theory.claims:
            dependencies = set(claim.dependencies)
            if claim.claim_id in dependencies:
                raise ValueError(f"claim {claim.claim_id} cannot depend on itself")
            unknown_dependencies = dependencies - known
            if unknown_dependencies:
                raise ValueError(
                    f"claim {claim.claim_id} has unknown dependencies: "
                    f"{sorted(unknown_dependencies)}"
                )
        dependencies_by_claim = {
            claim.claim_id: set(claim.dependencies) for claim in self.theory.claims
        }
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(claim_id: str) -> None:
            if claim_id in visiting:
                raise ValueError("theory claim dependency graph must be acyclic")
            if claim_id in visited:
                return
            visiting.add(claim_id)
            for dependency in dependencies_by_claim[claim_id]:
                visit(dependency)
            visiting.remove(claim_id)
            visited.add(claim_id)

        for claim_id in claim_ids:
            visit(claim_id)
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
        theory_progress_claims = {
            claim_id for unit in self.theory.progress for claim_id in unit.claim_ids
        }
        checked_claims = {
            claim_id for check in self.verification.checks for claim_id in check.claim_ids
        }
        unchecked_progress = theory_progress_claims - checked_claims
        if unchecked_progress:
            raise ValueError(
                "every theory progress claim requires an independent verification check: "
                f"{sorted(unchecked_progress)}"
            )
        theory_paths = {
            artifact.path for unit in self.theory.progress for artifact in unit.evidence
        }
        verification_paths = {
            artifact.path for check in self.verification.checks for artifact in check.evidence
        }
        verification_paths.update(
            artifact.path for unit in self.verification.progress for artifact in unit.evidence
        )
        shared_paths = theory_paths & verification_paths
        if shared_paths:
            raise ValueError(
                "theory and verification lanes require distinct evidence files: "
                f"{sorted(shared_paths)}"
            )
        progress_ids = [
            unit.unit_id for unit in (*self.theory.progress, *self.verification.progress)
        ]
        if len(progress_ids) != len(set(progress_ids)):
            raise ValueError("progress unit IDs must be unique across both lanes")
        check_ids = [check.check_id for check in self.verification.checks]
        if len(check_ids) != len(set(check_ids)):
            raise ValueError("verification check IDs must be unique")
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
