from unittest.mock import patch

import pytest
from app import app as flask_app
from flask import url_for

# Importing Flask application under test
from raspi_zero.app import app as flask_app


@pytest.fixture
def app():
    """
    Fixture to initialize the Flask application for tests.
    """
    yield flask_app


@pytest.fixture
def client(app):
    """
    Fixture to provide a test client for the Flask application.
    """
    return app.test_client()


@patch("hardware_control.HardwareControl.get_lamp_pin_status")
def test_lamp_status(mock_get_lamp_pin_status, client):
    """
    Test the /lamp-status/ route.
    """
    # Mock get_lamp_pin_status to return "ON"
    mock_get_lamp_pin_status.return_value = "ON"

    response = client.get("/lamp-status/")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Load the JSON data from the response
    json_data = response.get_json()

    # Assert that the lamp status in the response is "ON"
    assert json_data == {"lamp_pin_status": "ON"}

    # Optionally, you can repeat the process for when the lamp is "OFF"
    # by setting mock_get_lamp_pin_status.return_value = "OFF"
    # and making another request/assertion block here.


# import json
# from unittest.mock import patch

# import pytest

# from ..hardware_control import HardwareControl


# @pytest.fixture
# def gpio_mock(mocker):
#     """
#     Fixture to mock the RPi.GPIO module.
#     """
#     mock = mocker.patch("your_flask_app_module.RPi.GPIO")
#     return mock


# def test_turn_lamp_on(gpio_mock):
#     """
#     Test the turn_lamp_on method.
#     """
#     lamp_control_pin = 17  # Example pin number
#     hc = HardwareControl(lamp_control_pin)
#     hc.turn_lamp_on()
#     gpio_mock.output.assert_called_once_with(lamp_control_pin, gpio_mock.HIGH)


# def test_turn_lamp_off(gpio_mock):
#     """
#     Test the turn_lamp_off method.
#     """
#     lamp_control_pin = 17  # Example pin number
#     hc = HardwareControl(lamp_control_pin)
#     hc.turn_lamp_off()
#     gpio_mock.output.assert_called_once_with(lamp_control_pin, gpio_mock.LOW)


# def test_get_lamp_pin_status(gpio_mock):
#     """
#     Test the get_lamp_pin_status method.
#     """
#     lamp_control_pin = 17  # Example pin number
#     hc = HardwareControl(lamp_control_pin)
#     # Simulate lamp is on
#     gpio_mock.input.return_value = 1
#     assert hc.get_lamp_pin_status() == "ON"
#     # Simulate lamp is off
#     gpio_mock.input.return_value = 0
#     assert hc.get_lamp_pin_status() == "OFF"


# def test_home_redirect(client):
#     response = client.get("/")
#     assert response.status_code == 302
#     assert "/gpio/" in response.location


# def test_gpio_home(client):
#     response = client.get("/gpio/")
#     assert response.status_code == 200
#     assert "Pin 17 Up" in response.data.decode()


# @patch(
#     "raspi_zero.hardware_control.HardwareControl.get_lamp_status", return_value="OFF"
# )
# def test_lamp_status_off(mock_get_lamp_status, client):
#     response = client.get("/lamp-status/")
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert data["lamp_pin_status"] == "OFF"


# @patch("raspi_zero.hardware_control.HardwareControl.get_lamp_status", return_value="ON")
# def test_lamp_status_on(mock_get_lamp_status, client):
#     response = client.get("/lamp-status/")
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert data["lamp_pin_status"] == "ON"
