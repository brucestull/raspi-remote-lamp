# raspi_zero\mocks\mock_gpio.py


class MockGPIO:
    BCM = "BCM"
    OUT = "OUT"
    LOW = 0
    HIGH = 1

    def __init__(self):
        self.pin_states = {}

    def setmode(self, mode):
        pass  # Mode setting can be ignored for mocking

    def setup(self, pin, mode, initial=0):
        self.pin_states[pin] = initial

    def input(self, pin):
        return self.pin_states.get(pin, self.LOW)

    def output(self, pin, state):
        self.pin_states[pin] = state
