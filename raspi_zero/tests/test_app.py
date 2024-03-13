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


@patch("app.GPIO.input", return_value=0)
def test_lamp_status_off(mock_gpio_input, client):
    response = client.get("/lamp-status/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["lamp_pin_status"] == "OFF"


@patch("app.GPIO.input", return_value=1)
def test_lamp_status_on(mock_gpio_input, client):
    response = client.get("/lamp-status/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["lamp_pin_status"] == "ON"
