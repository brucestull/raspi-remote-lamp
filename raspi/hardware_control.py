import RPi.GPIO as GPIO


class HardwareControl:
    """
    A class to control the hardware of the Raspberry Pi Zero.

    Attributes:
        control_pin (int): The BCM pin number for the pin control.
    """

    def __init__(self, control_pin):
        self.control_pin = control_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.control_pin, GPIO.OUT, initial=GPIO.LOW)

    def get_pin_status(self):
        """
        Get the status of the pin.

        Returns:
            str: The status of the pin.
        """
        pin_status_binary = GPIO.input(self.control_pin)
        if pin_status_binary == 0:
            return "OFF"
        elif pin_status_binary == 1:
            return "ON"
        else:
            return "UNKNOWN"
        # Alternate implementation:
        # if pin_status_binary == 0:
        #     pin_status_str = "OFF"
        # elif pin_status_binary == 1:
        #     pin_status_str = "ON"
        # else:
        #     pin_status_str = "UNKNOWN"
        # return pin_status_str

    def turn_pin_on(self):
        """
        Turn the pin on.
        """
        GPIO.output(self.control_pin, GPIO.HIGH)
        return "Pin turned on."

    def turn_pin_off(self):
        """
        Turn the pin off.
        """
        GPIO.output(self.control_pin, GPIO.LOW)
        return "Pin turned off."

    def toggle_pin(self):
        """
        Toggle the pin on or off.
        """
        pin_status_binary = GPIO.input(self.control_pin)
        if pin_status_binary == 0:
            GPIO.output(self.control_pin, GPIO.HIGH)
            return "Pin turned on."
        elif pin_status_binary == 1:
            GPIO.output(self.control_pin, GPIO.LOW)
            return "Pin turned off."
        else:
            return "Pin status unknown."

    def __str__(self):
        return f"Hardware Pin {self.control_pin}: Status {self.get_pin_status()}"
