# test_app.py
def test_turn_on_17(client, mock_rpi_gpio):
    response = client.get("/gpio/17/on")
    assert response.data.decode() == "Relay on BCM pin 17 turned on"
    mock_rpi_gpio.setup.assert_called_once_with(17, mock_rpi_gpio.OUT)
    mock_rpi_gpio.output.assert_called_once_with(17, mock_rpi_gpio.HIGH)


def test_turn_off_18(client, mock_rpi_gpio):
    response = client.get("/gpio/18/off")
    assert response.data.decode() == "Relay on BCM pin 18 turned off"
    mock_rpi_gpio.setup.assert_called_once_with(18, mock_rpi_gpio.OUT)
    mock_rpi_gpio.output.assert_called_once_with(18, mock_rpi_gpio.LOW)
