# test_modules\led_tests.py

from time import sleep

from machine import Pin
from picozero import pico_led

status = pico_led

# Setup LED pins:
startup_led = Pin(20, Pin.OUT)
wifi_status_led = Pin(19, Pin.OUT)
lamp_on = Pin(18, Pin.OUT)
lamp_off = Pin(17, Pin.OUT)
shutdown_led = Pin(16, Pin.OUT)


def pin_cycle(pin, time_diff, cycles):
    for _ in range(cycles):
        pin.on()
        sleep(time_diff)
        pin.off()
        sleep(time_diff)


def test_leds():
    pin_cycle(status, 0.1, 4)
    pin_cycle(startup_led, 0.1, 4)
    pin_cycle(wifi_status_led, 0.1, 4)
    pin_cycle(lamp_on, 0.1, 4)
    pin_cycle(lamp_off, 0.1, 4)
    pin_cycle(shutdown_led, 0.1, 4)


if __name__ == "__main__":
    test_leds()
