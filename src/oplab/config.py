from __future__ import annotations

import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

from oplab.errors import ConfigurationError
from oplab.hashing import sha256_bytes


class EligibilityConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    statuses: tuple[str, ...]
    max_difficulty: int = Field(ge=1, le=5)
    excluded_statement_statuses: tuple[str, ...]


class WeightConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    tractability: float = Field(ge=0)
    statement_quality: float = Field(ge=0)
    provenance: float = Field(ge=0)
    literature_freshness: float = Field(ge=0)
    research_traction: float = Field(ge=0)
    computational_affordance: float = Field(ge=0)

    @model_validator(mode="after")
    def weights_sum_to_one(self) -> WeightConfig:
        total = sum(self.model_dump().values())
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"ranking weights must sum to 1.0; found {total}")
        return self


class FreshnessConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    fresh_days: int = Field(ge=0)
    aging_days: int = Field(ge=0)
    fresh: float = Field(ge=0, le=1)
    aging: float = Field(ge=0, le=1)
    stale: float = Field(ge=0, le=1)
    missing: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def thresholds_are_ordered(self) -> FreshnessConfig:
        if self.aging_days < self.fresh_days:
            raise ValueError("aging_days must be greater than or equal to fresh_days")
        return self


class KeywordConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    computational: tuple[str, ...]


class RankingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    version: int = Field(ge=1)
    eligibility: EligibilityConfig
    weights: WeightConfig
    difficulty: dict[str, float]
    statement_quality: dict[str, float]
    research_traction: dict[str, float]
    freshness: FreshnessConfig
    keywords: KeywordConfig


def load_ranking_config(path: Path) -> tuple[RankingConfig, str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ConfigurationError(f"cannot read ranking config {path}: {exc}") from exc
    try:
        config = RankingConfig.model_validate(tomllib.loads(raw.decode("utf-8")))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError, ValueError) as exc:
        raise ConfigurationError(f"invalid ranking config {path}: {exc}") from exc
    return config, sha256_bytes(raw)
