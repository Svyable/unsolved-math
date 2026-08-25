from pathlib import Path

import pytest


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def fixture_path(project_root: Path) -> Path:
    return project_root / "tests" / "fixtures" / "problems.json"
