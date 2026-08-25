from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from oplab.cycle_store import (
    build_cycle_manifest,
    validate_cycle_directory,
    verify_cycle_manifest,
)
from oplab.hashing import canonical_json_bytes, sha256_bytes, sha256_file
from oplab.research import (
    ArtifactRef,
    ClaimOrigin,
    ClaimStatus,
    FrozenProblemSnapshot,
    ProgressKind,
    ProgressUnit,
    ResearchClaim,
    ResearchConclusion,
    ResearchCycle,
    TheoryLane,
    VerificationCheck,
    VerificationLane,
    VerificationMethod,
)


def _artifact(cycle_dir: Path, name: str) -> ArtifactRef:
    return ArtifactRef(path=name, sha256=sha256_file(cycle_dir / name), media_type="text/markdown")


def _cycle(cycle_dir: Path, *, target: str = "Test one bounded synthetic claim.") -> ResearchCycle:
    theory_artifact = _artifact(cycle_dir, "theory.md")
    verification_artifact = _artifact(cycle_dir, "verification.md")
    claim = ResearchClaim(
        claim_id="claim-1",
        statement="The bounded test agrees with the candidate invariant.",
        status=ClaimStatus.EXPERIMENTALLY_SUPPORTED,
        origin=ClaimOrigin.DERIVED,
        falsification_condition="One enumerated object violates the invariant.",
    )
    frozen_statement = "Test a bounded synthetic conjecture without a parent-problem claim."
    return ResearchCycle(
        cycle_id="20260825T230000Z-example",
        problem_id="EXAMPLE-001",
        frozen_problem=FrozenProblemSnapshot(
            problem_id="EXAMPLE-001",
            title="Synthetic fixture",
            statement=frozen_statement,
            statement_sha256=sha256_bytes(frozen_statement.encode("utf-8")),
            upstream_dataset="local/test-fixture",
            upstream_revision="fixture-revision",
            upstream_file_sha256="0" * 64,
            frozen_at=datetime(2026, 8, 25, 22, 59, tzinfo=UTC),
            source_urls=("https://example.test/fixture", "https://example.test/method"),
            imported_status="open",
            selection_basis="Synthetic fixture; not ranked.",
        ),
        started_at=datetime(2026, 8, 25, 23, 0, tzinfo=UTC),
        completed_at=datetime(2026, 8, 25, 23, 45, tzinfo=UTC),
        selection_basis="Synthetic fixture selected for contract verification.",
        theory=TheoryLane(
            target=target,
            definitions=("Define the finite search domain.",),
            assumptions=("Object size is at most eight.",),
            approaches_considered=("Enumeration", "Invariant argument"),
            falsification_targets=("Search all boundary objects.",),
            claims=(claim,),
            progress=(
                ProgressUnit(
                    unit_id="theory-1",
                    kind=ProgressKind.REPRODUCIBLE_EXPERIMENT,
                    summary="Enumeration separates the candidate invariants.",
                    claim_ids=(claim.claim_id,),
                    evidence=(theory_artifact,),
                ),
            ),
        ),
        verification=VerificationLane(
            checks=(
                VerificationCheck(
                    check_id="check-1",
                    claim_ids=(claim.claim_id,),
                    method_family=VerificationMethod.INDEPENDENT_IMPLEMENTATION,
                    method="Independent boundary enumeration",
                    independent_context=True,
                    independence_basis="Separate implementation using only the frozen target.",
                    result="The second implementation agrees only on the bounded domain.",
                    reproduction_command="python experiments/verify.py",
                    evidence=(verification_artifact,),
                    blocking_objections=("No universal step follows from finite checks.",),
                ),
            ),
            progress=(
                ProgressUnit(
                    unit_id="verification-1",
                    kind=ProgressKind.PROOF_GAP_IDENTIFIED,
                    summary="The universal extension is the exact unsupported step.",
                    claim_ids=(claim.claim_id,),
                    evidence=(verification_artifact,),
                ),
            ),
            unresolved_objections=("The extension beyond size eight is open in this fixture.",),
        ),
        conclusion=ResearchConclusion.CONTINUE,
        next_step="Test whether the invariant is preserved by one extension operation.",
    )


def test_cycle_requires_hashed_progress_in_both_lanes(tmp_path: Path) -> None:
    (tmp_path / "theory.md").write_text("bounded theory delta\n", encoding="utf-8")
    (tmp_path / "verification.md").write_text("independent verification delta\n", encoding="utf-8")
    (tmp_path / "experiments").mkdir()
    (tmp_path / "experiments" / "manifest.json").write_text(
        "nested experiment metadata\n", encoding="utf-8"
    )
    cycle = _cycle(tmp_path)
    (tmp_path / "cycle.json").write_bytes(canonical_json_bytes(cycle.model_dump(mode="json")))

    report = validate_cycle_directory(tmp_path)
    manifest = build_cycle_manifest(tmp_path)
    (tmp_path / "manifest.json").write_bytes(manifest)
    verified = verify_cycle_manifest(tmp_path)

    assert report.valid is True
    assert verified.valid is True
    assert cycle.material_progress is True
    assert b'"material_progress":true' in manifest
    assert b'"schema_version":2' in manifest
    assert b'"experiments/manifest.json"' in manifest


def test_cycle_rejects_autonomous_parent_problem_solve_claim(tmp_path: Path) -> None:
    (tmp_path / "theory.md").write_text("theory\n", encoding="utf-8")
    (tmp_path / "verification.md").write_text("verification\n", encoding="utf-8")

    with pytest.raises(ValidationError, match="solve claims are forbidden"):
        _cycle(tmp_path, target="The problem is solved by this argument.")


def test_manifest_detects_packet_change_after_signing(tmp_path: Path) -> None:
    (tmp_path / "theory.md").write_text("bounded theory delta\n", encoding="utf-8")
    (tmp_path / "verification.md").write_text(
        "independent verification delta\n", encoding="utf-8"
    )
    cycle = _cycle(tmp_path)
    (tmp_path / "cycle.json").write_bytes(canonical_json_bytes(cycle.model_dump(mode="json")))
    (tmp_path / "manifest.json").write_bytes(build_cycle_manifest(tmp_path))

    (tmp_path / "untracked-result.txt").write_text("late mutation\n", encoding="utf-8")

    report = verify_cycle_manifest(tmp_path)

    assert report.valid is False
    assert "does not exactly match" in " ".join(report.errors)
