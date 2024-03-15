# raspi_zero\hardware_control.py

import RPi.GPIO as GPIO


class HardwareControl:
    """
    A class to control the hardware of the Raspberry Pi Zero.

    Attributes:
        lamp_control_pin (int): The BCM pin number for the lamp control.
    """

    def __init__(self, lamp_control_pin):
        self.lamp_control_pin = lamp_control_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.lamp_control_pin, GPIO.OUT, initial=GPIO.LOW)

    def get_lamp_pin_status(self):
        """
        Get the status of the lamp pin.

        Returns:
            str: The status of the lamp pin.
        """
        lamp_pin_status_binary = GPIO.input(self.lamp_control_pin)
        if lamp_pin_status_binary == 0:
            return "OFF"
        elif lamp_pin_status_binary == 1:
            return "ON"
        else:
            return "UNKNOWN"
        # Alternate implementation:
        # if lamp_pin_status_binary == 0:
        #     lamp_pin_status_str = "OFF"
        # elif lamp_pin_status_binary == 1:
        #     lamp_pin_status_str = "ON"
        # else:
        #     lamp_pin_status_str = "UNKNOWN"
        # return lamp_pin_status_str

    def turn_lamp_on(self):
        """
        Turn the lamp on.
        """
        GPIO.output(self.lamp_control_pin, GPIO.HIGH)
        return "Lamp turned on."

    def turn_lamp_off(self):
        """
        Turn the lamp off.
        """
        GPIO.output(self.lamp_control_pin, GPIO.LOW)
        return "Lamp turned off."
