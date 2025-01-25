from pathlib import Path

import pytest


@pytest.fixture
def project_root() -> str:
    return str(Path(__file__).parent.parent)
