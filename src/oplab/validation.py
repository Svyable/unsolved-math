from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from oplab.artifacts import read_model_jsonl
from oplab.config import load_ranking_config
from oplab.hashing import sha256_file
from oplab.models import (
    ClaimTrust,
    NormalizedProblem,
    RankedProblem,
    SourceManifest,
    ValidationReport,
)
from oplab.ranking import is_research_eligible


def validate_repository(repo_root: Path) -> ValidationReport:
    checks: list[str] = []
    errors: list[str] = []
    manifest_path = repo_root / "data" / "current" / "manifest.json"
    if not manifest_path.exists():
        return ValidationReport(
            valid=False,
            checks=(),
            errors=("no current manifest; run `oplab sync` first",),
        )
    try:
        manifest = SourceManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValidationError, ValueError) as exc:
        return ValidationReport(valid=False, checks=(), errors=(f"invalid manifest: {exc}",))

    for relative_path, expected_hash in sorted(manifest.artifacts.items()):
        artifact_path = repo_root / relative_path
        if not artifact_path.is_file():
            errors.append(f"missing artifact: {relative_path}")
            continue
        actual_hash = sha256_file(artifact_path)
        if actual_hash != expected_hash:
            errors.append(
                f"artifact hash mismatch for {relative_path}: "
                f"expected {expected_hash}, found {actual_hash}"
            )
    if not errors:
        checks.append(f"verified {len(manifest.artifacts)} artifact hashes")

    try:
        problems = read_model_jsonl(
            repo_root / "data" / "current" / "problems.jsonl", NormalizedProblem
        )
    except RuntimeError as exc:
        errors.append(str(exc))
        problems = []
    if len(problems) != manifest.record_count:
        errors.append(
            f"manifest record count {manifest.record_count} "
            f"does not match index count {len(problems)}"
        )
    else:
        checks.append(f"index contains {len(problems)} records")
    if any(problem.claim_trust != ClaimTrust.UNVERIFIED_EXTERNAL_METADATA for problem in problems):
        errors.append("one or more imported records escaped the unverified claim boundary")
    else:
        checks.append("all imported records remain explicitly unverified")

    config, config_hash = load_ranking_config(repo_root / "config" / "ranking.toml")
    if config_hash != manifest.ranking_config_sha256:
        errors.append("ranking configuration changed after the current queues were generated")
    else:
        checks.append("ranking configuration hash matches the manifest")

    problem_by_id = {problem.problem_id: problem for problem in problems}
    research_path = repo_root / "data" / "queues" / "research.json"
    try:
        payload = json.loads(research_path.read_text(encoding="utf-8"))
        raw_items = payload.get("items", []) if isinstance(payload, dict) else []
        ranked_items = [RankedProblem.model_validate(item) for item in raw_items]
    except (OSError, json.JSONDecodeError, ValidationError, ValueError) as exc:
        errors.append(f"invalid research queue: {exc}")
        ranked_items = []
    for ranked in ranked_items:
        problem = problem_by_id.get(ranked.problem_id)
        if problem is None:
            errors.append(f"research queue references unknown problem {ranked.problem_id}")
            continue
        eligible, reason = is_research_eligible(problem, config)
        if not eligible:
            errors.append(f"ineligible research queue entry {ranked.problem_id}: {reason}")
        if ranked.imported_status == "solved":
            errors.append(f"solved imported record entered research queue: {ranked.problem_id}")
    if ranked_items and not any("research queue" in error for error in errors):
        checks.append(f"research gate holds for {len(ranked_items)} ranked entries")

    return ValidationReport(valid=not errors, checks=tuple(checks), errors=tuple(errors))
