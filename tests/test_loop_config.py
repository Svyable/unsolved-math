from pathlib import Path

import pytest

from oplab.errors import ConfigurationError
from oplab.loop_config import load_research_loop_config


def test_publication_policy_is_ready_and_autonomous(project_root: Path) -> None:
    config, _ = load_research_loop_config(project_root / "config" / "research-loop.toml")

    assert config.publication.branch == "automation/hourly-research-loop"
    assert config.publication.pull_request_state == "ready"
    assert config.publication.merge_method == "merge"
    assert config.publication.autonomous_merge is True
    assert config.publication.require_successful_ci is True
    assert config.publication.require_mergeable_head is True
    assert config.publication.verify_merged_main is True


@pytest.mark.parametrize(
    "gate",
    [
        "autonomous_merge",
        "require_successful_ci",
        "require_mergeable_head",
        "verify_merged_main",
    ],
)
def test_publication_policy_rejects_disabled_gate(
    project_root: Path, tmp_path: Path, gate: str
) -> None:
    source = (project_root / "config" / "research-loop.toml").read_text(encoding="utf-8")
    altered = source.replace(f"{gate} = true", f"{gate} = false")
    path = tmp_path / "research-loop.toml"
    path.write_text(altered, encoding="utf-8")

    with pytest.raises(ConfigurationError, match="publication gates disabled"):
        load_research_loop_config(path)
