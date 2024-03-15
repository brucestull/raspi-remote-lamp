# tests/test_hardware_control.py

import unittest
from unittest.mock import patch
import sys

# Import the mock module directly, and patch sys.modules to replace RPi.GPIO with MockGPIO
from mocks.mock_gpio import MockGPIO


class TestHardwareControl(unittest.TestCase):
    def setUp(self):
        # Patch sys.modules to replace RPi.GPIO with MockGPIO before any import happens
        sys.modules["RPi.GPIO"] = MockGPIO()

        # Now that RPi.GPIO is mocked, you can safely import your module
        global HardwareControl
        from hardware_control import HardwareControl

    def test_turn_lamp_on(self):
        hardware = HardwareControl(17)
        hardware.turn_lamp_on()
        self.assertEqual(hardware.get_lamp_pin_status(), "ON")

    def test_turn_lamp_off(self):
        hardware = HardwareControl(17)
        hardware.turn_lamp_off()
        self.assertEqual(hardware.get_lamp_pin_status(), "OFF")


if __name__ == "__main__":
    unittest.main()
