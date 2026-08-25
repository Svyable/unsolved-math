import pytest

from oplab.errors import NetworkPermissionError
from oplab.sources import HuggingFaceSource


def test_network_requires_explicit_permission() -> None:
    with pytest.raises(NetworkPermissionError):
        HuggingFaceSource(revision="main", allow_network=False).fetch()
