from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from oplab.errors import IntegrityError
from oplab.hashing import canonical_json_bytes, sha256_file
from oplab.models import ValidationReport
from oplab.research import ResearchCycle


def load_cycle(cycle_dir: Path) -> ResearchCycle:
    cycle_path = cycle_dir / "cycle.json"
    try:
        return ResearchCycle.model_validate_json(cycle_path.read_text(encoding="utf-8"))
    except (OSError, ValidationError, ValueError) as exc:
        raise IntegrityError(f"invalid research cycle {cycle_path}: {exc}") from exc


def validate_cycle_directory(cycle_dir: Path) -> ValidationReport:
    checks: list[str] = []
    errors: list[str] = []
    try:
        cycle = load_cycle(cycle_dir)
    except IntegrityError as exc:
        return ValidationReport(valid=False, checks=(), errors=(str(exc),))
    root = cycle_dir.resolve()
    for candidate in cycle_dir.rglob("*"):
        if candidate.is_symlink():
            relative = candidate.relative_to(cycle_dir)
            errors.append(f"symlinks are forbidden in cycle packets: {relative}")
    for artifact in cycle.artifact_refs():
        path = (cycle_dir / artifact.path).resolve()
        if not path.is_relative_to(root):
            errors.append(f"artifact escapes cycle directory: {artifact.path}")
            continue
        if not path.is_file():
            errors.append(f"missing cycle artifact: {artifact.path}")
            continue
        actual = sha256_file(path)
        if actual != artifact.sha256:
            errors.append(
                f"artifact hash mismatch for {artifact.path}: "
                f"expected {artifact.sha256}, found {actual}"
            )
    if not errors:
        checks.append(f"verified {len(cycle.artifact_refs())} cycle artifact references")
    if cycle.material_progress:
        checks.append("theory and independent-verification lanes both contain progress units")
    else:
        errors.append("cycle does not contain material progress in both required lanes")
    return ValidationReport(valid=not errors, checks=tuple(checks), errors=tuple(errors))


def build_cycle_manifest(cycle_dir: Path) -> bytes:
    cycle = load_cycle(cycle_dir)
    files: dict[str, str] = {}
    for path in sorted(cycle_dir.rglob("*")):
        if path.is_symlink():
            raise IntegrityError(
                f"symlinks are forbidden in cycle packets: {path.relative_to(cycle_dir)}"
            )
        if not path.is_file() or path == cycle_dir / "manifest.json":
            continue
        relative = path.relative_to(cycle_dir).as_posix()
        files[relative] = sha256_file(path)
    payload = {
        "schema_version": 2,
        "cycle_id": cycle.cycle_id,
        "problem_id": cycle.problem_id,
        "cycle_sha256": sha256_file(cycle_dir / "cycle.json"),
        "files": files,
        "material_progress": cycle.material_progress,
        "conclusion": cycle.conclusion,
    }
    return canonical_json_bytes(payload)


def verify_cycle_manifest(cycle_dir: Path) -> ValidationReport:
    """Verify the cycle contract and the exact immutable packet manifest."""

    base = validate_cycle_directory(cycle_dir)
    checks = list(base.checks)
    errors = list(base.errors)
    manifest_path = cycle_dir / "manifest.json"
    if not manifest_path.is_file():
        errors.append("missing cycle manifest: manifest.json")
    elif not errors:
        try:
            expected = build_cycle_manifest(cycle_dir)
            actual = manifest_path.read_bytes()
        except (OSError, IntegrityError) as exc:
            errors.append(f"cannot verify cycle manifest: {exc}")
        else:
            if actual != expected:
                errors.append(
                    "cycle manifest does not exactly match the current packet; rebuild it"
                )
            else:
                checks.append("verified canonical manifest over every packet file")
    return ValidationReport(valid=not errors, checks=tuple(checks), errors=tuple(errors))


def read_cycle_manifest(cycle_dir: Path) -> dict[str, object]:
    try:
        value = json.loads((cycle_dir / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(f"invalid cycle manifest in {cycle_dir}: {exc}") from exc
    if not isinstance(value, dict):
        raise IntegrityError("cycle manifest must be a JSON object")
    return value
