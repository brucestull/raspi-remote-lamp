# tests/test_hardware_control.py

import unittest
from unittest.mock import patch

from mocks.mock_gpio import MockGPIO

# Patch 'RPi.GPIO' in sys.modules
with patch.dict("sys.modules", {"RPi.GPIO": MockGPIO}):
    # Now that 'RPi.GPIO' is mocked, you can safely import your module
    from hardware_control import HardwareControl


class TestHardwareControl(unittest.TestCase):
    def test_turn_lamp_on(self):
        hardware = HardwareControl(17)
        hardware.turn_lamp_on()
        # Ensure the lamp's status is "ON" after the method call
        self.assertEqual(hardware.get_lamp_pin_status(), "ON")

    def test_turn_lamp_off(self):
        hardware = HardwareControl(17)
        hardware.turn_lamp_off()
        # Ensure the lamp's status is "OFF" after the method call
        self.assertEqual(hardware.get_lamp_pin_status(), "OFF")


if __name__ == "__main__":
    unittest.main()
