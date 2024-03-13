# raspi_zero\tests\conftest.py
import pytest
from unittest.mock import MagicMock, patch
from raspi_zero.app import app


@pytest.fixture(autouse=True)
def mock_gpio():
    with patch.dict("sys.modules", {"RPi.GPIO": MagicMock()}):
        yield


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
