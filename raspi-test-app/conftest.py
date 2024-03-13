# conftest.py
import pytest
from unittest.mock import MagicMock
from app import app as flask_app


@pytest.fixture(autouse=True)
def mock_rpi_gpio(monkeypatch):
    mock_gpio = MagicMock()
    monkeypatch.setattr("RPi.GPIO", mock_gpio)
    return mock_gpio


@pytest.fixture
def app():
    flask_app.config.update({"TESTING": True})
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()
