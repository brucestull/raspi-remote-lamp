import json
from unittest.mock import patch


def test_home_redirect(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/gpio/" in response.location


def test_gpio_home(client):
    response = client.get("/gpio/")
    assert response.status_code == 200
    assert "Pin 17 Up" in response.data.decode()


@patch(
    "raspi_zero.hardware_control.HardwareControl.get_lamp_status", return_value="OFF"
)
def test_lamp_status_off(mock_get_lamp_status, client):
    response = client.get("/lamp-status/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["lamp_pin_status"] == "OFF"


@patch("raspi_zero.hardware_control.HardwareControl.get_lamp_status", return_value="ON")
def test_lamp_status_on(mock_get_lamp_status, client):
    response = client.get("/lamp-status/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["lamp_pin_status"] == "ON"
