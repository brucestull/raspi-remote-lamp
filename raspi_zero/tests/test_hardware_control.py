# tests/test_hardware_control.py

import importlib
import unittest
from unittest.mock import patch

from mocks.mock_gpio import MockGPIO


class TestHardwareControl(unittest.TestCase):
    @patch.dict("sys.modules", {"RPi.GPIO": MockGPIO})
    def test_turn_lamp_on(self):
        # Dynamically import the HardwareControl class
        hardware_module = importlib.import_module("hardware_control")
        HardwareControl = getattr(hardware_module, "HardwareControl")

        hardware = HardwareControl(17)
        hardware.turn_lamp_on()
        self.assertEqual(hardware.get_lamp_pin_status(), "ON")

    @patch.dict("sys.modules", {"RPi.GPIO": MockGPIO})
    def test_turn_lamp_off(self):
        # Dynamically import the HardwareControl class
        hardware_module = importlib.import_module("hardware_control")
        HardwareControl = getattr(hardware_module, "HardwareControl")

        hardware = HardwareControl(17)
        hardware.turn_lamp_off()
        self.assertEqual(hardware.get_lamp_pin_status(), "OFF")


if __name__ == "__main__":
    unittest.main()
