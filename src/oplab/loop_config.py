from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from oplab.errors import ConfigurationError
from oplab.hashing import sha256_bytes


class SelectionConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    queue: Literal["research"]
    top_k: int = Field(ge=1, le=1000)
    cooldown_hours: int = Field(ge=1, le=24 * 90)
    max_consecutive_cycles_per_problem: int = Field(ge=1, le=10)


class BudgetConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    wall_clock_minutes: int = Field(ge=5, le=60)
    model_tokens: int = Field(ge=1000, le=200000)
    subprocesses: int = Field(ge=1, le=64)
    disk_megabytes: int = Field(ge=32, le=4096)
    network_access: Literal["disabled", "allowlisted-primary-sources-only"]


class RequirementConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    cycle_schema_version: Literal[2]
    theory_progress_units: int = Field(ge=1)
    verification_progress_units: int = Field(ge=1)
    independent_verification_checks: int = Field(ge=1)
    counterexample_search_first: bool
    distinct_evidence_paths: bool
    verified_packet_manifest: bool
    human_review_before_merge: bool

    @model_validator(mode="after")
    def review_gate_cannot_be_disabled(self) -> RequirementConfig:
        required = {
            "counterexample_search_first": self.counterexample_search_first,
            "distinct_evidence_paths": self.distinct_evidence_paths,
            "verified_packet_manifest": self.verified_packet_manifest,
            "human_review_before_merge": self.human_review_before_merge,
        }
        disabled = sorted(name for name, enabled in required.items() if not enabled)
        if disabled:
            raise ValueError(f"non-negotiable research boundaries disabled: {disabled}")
        return self


class ResearchLoopConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    version: int = Field(ge=1)
    selection: SelectionConfig
    budgets: BudgetConfig
    requirements: RequirementConfig


def load_research_loop_config(path: Path) -> tuple[ResearchLoopConfig, str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ConfigurationError(f"cannot read research-loop config {path}: {exc}") from exc
    try:
        config = ResearchLoopConfig.model_validate(tomllib.loads(raw.decode("utf-8")))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError, ValueError) as exc:
        raise ConfigurationError(f"invalid research-loop config {path}: {exc}") from exc
    return config, sha256_bytes(raw)
