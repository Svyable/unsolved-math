from pathlib import Path
from shutil import copy2, copytree

import pytest


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def fixture_path(project_root: Path) -> Path:
    return project_root / "tests" / "fixtures" / "problems.json"


@pytest.fixture
def bootstrap_root(tmp_path: Path, project_root: Path) -> Path:
    """An explicitly unsynchronized repo, independent of tracked live queues."""
    for directory in ("config", "docs", "prompts", "cases/COMB-001"):
        copytree(project_root / directory, tmp_path / directory)
    for filename in ("AGENTS.md", "README.md", "data/research-loop/history.jsonl"):
        target = tmp_path / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(project_root / filename, target)
    assert not (tmp_path / "data/queues/research.json").exists()
    return tmp_path
