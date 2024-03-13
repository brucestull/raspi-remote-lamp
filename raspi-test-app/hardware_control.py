# raspi-test-app\hardware_control.py
try:
    import RPi.GPIO as GPIO
except ImportError:
    # Create a basic mock of the RPi.GPIO interface for non-Raspberry Pi environments
    class MockGPIO:
        BCM = "BCM"
        OUT = "OUT"
        HIGH = "HIGH"
        LOW = "LOW"

        @staticmethod
        def setmode(*args, **kwargs):
            pass

        @staticmethod
        def setup(*args, **kwargs):
            pass

        @staticmethod
        def output(*args, **kwargs):
            pass

        @staticmethod
        def cleanup(*args, **kwargs):
            pass

    GPIO = MockGPIO


class HardwareControl:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    def turn_on_relay(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

    def turn_off_relay(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
