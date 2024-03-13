import pytest

# from your_flask_app_file import app  # Adjust the import path as necessary
from raspi_zero.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
