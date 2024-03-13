import RPi.GPIO as GPIO

# BCM pin number for the lamp control:
lamp_control_pin = 17


class HardwareControl:
    def __init__(self):
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(lamp_control_pin, GPIO.OUT, initial=GPIO.LOW)

    def turn_on_lamp(self):
        GPIO.output(lamp_control_pin, GPIO.HIGH)

    def turn_off_lamp(self):
        GPIO.output(lamp_control_pin, GPIO.LOW)

    def get_lamp_status(self):
        lamp_pin_status_bin = GPIO.input(lamp_control_pin)
        if lamp_pin_status_bin == 0:
            return "OFF"
        elif lamp_pin_status_bin == 1:
            return "ON"
        else:
            return "UNKNOWN"
