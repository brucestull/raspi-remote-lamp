# tests/test_hardware_control.py

from unittest.mock import patch
import unittest

# You may need to adjust the import path based on your project structure
from hardware_control import HardwareControl
from mocks.mock_gpio import (
    MockGPIO,
)  # Adjust the import path based on your actual file location


class TestHardwareControl(unittest.TestCase):

    @patch("raspi_zero.hardware_control.GPIO", new=MockGPIO())
    def test_turn_lamp_on(self):
        hardware = HardwareControl(17)
        hardware.turn_lamp_on()
        self.assertEqual(hardware.get_lamp_pin_status(), "ON")

    @patch("raspi_zero.hardware_control.GPIO", new=MockGPIO())
    def test_turn_lamp_off(self):
        hardware = HardwareControl(17)
        hardware.turn_lamp_off()
        self.assertEqual(hardware.get_lamp_pin_status(), "OFF")


if __name__ == "__main__":
    unittest.main()
