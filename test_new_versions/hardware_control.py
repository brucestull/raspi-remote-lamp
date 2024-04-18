import RPi.GPIO as GPIO


class GPIOPin:
    """
    A class to control the hardware pins of the Raspberry Pi Zero.
    - Default `number_mode` is `GPIO.BCM`.
    - Default `output_mode` is `GPIO.OUT`.
    - Default `initial_state` state is `LOW`.

    Attributes:
        pin (int): The BCM pin number to be controlled.
    """

    def __init__(
        self, pin, number_mode=GPIO.BCM, output_mode=GPIO.OUT, initial_state=GPIO.LOW
    ):
        self.pin = pin
        GPIO.setmode(number_mode)
        GPIO.setup(self.pin, output_mode, initial_state)

    def get_pin_status(self):
        """
        Get the status of the pin.

        Returns:
            str: The status of the pin. Either "OFF", "ON", or "UNKNOWN".
        """
        pin_status = GPIO.input(self.pin)
        if pin_status == 0:
            return "OFF"
        elif pin_status == 1:
            return "ON"
        else:
            return "UNKNOWN"

    def pin_on(self):
        """
        Turn the pin on.

        Returns:
            str: A message indicating the pin is set to on.
        """
        GPIO.output(self.pin, GPIO.HIGH)
        return "Pin set to on."

    def pin_off(self):
        """
        Turn the pin off.

        Returns:
            str: A message indicating the pin is set to off.
        """
        GPIO.output(self.pin, GPIO.LOW)
        return "Pin set to off."

    def toggle_pin(self):
        """
        Toggle the pin on or off.

        Returns:
            str: A message indicating the pin is toggled on or off, or unknown.
        """
        pin_status_binary = GPIO.input(self.pin)
        if pin_status_binary == 0:
            GPIO.output(self.pin, GPIO.HIGH)
            return "Pin toggled on."
        elif pin_status_binary == 1:
            GPIO.output(self.pin, GPIO.LOW)
            return "Pin toggled off."
        else:
            return "Pin status unknown."
