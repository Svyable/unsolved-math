import json
from pathlib import Path

from oplab.config import load_ranking_config
from oplab.models import ClaimTrust
from oplab.normalization import normalize_problem


def test_normalization_marks_external_claims_and_untrusted_content(
    project_root: Path, fixture_path: Path
) -> None:
    config, _ = load_ranking_config(project_root / "config" / "ranking.toml")
    records = json.loads(fixture_path.read_text(encoding="utf-8"))

    good = normalize_problem(records[0], config)
    suspicious = normalize_problem(records[3], config)

    assert good.problem_id == "GOOD-001"
    assert good.claim_trust == ClaimTrust.UNVERIFIED_EXTERNAL_METADATA
    assert good.computational_keywords == ("bound", "coloring", "finite", "graph")
    assert suspicious.suspicious_content is True
    assert "rm -rf" not in suspicious.model_dump_json()
