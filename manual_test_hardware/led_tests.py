# test_modules\led_tests.py

from time import sleep

from machine import Pin
from picozero import pico_led

status = pico_led

boot = Pin(16, Pin.OUT)
wifi = Pin(17, Pin.OUT)
led_on = Pin(18, Pin.OUT)
led_off = Pin(19, Pin.OUT)


def pin_cycle(pin, time_diff, cycles):
    for _ in range(cycles):
        pin.on()
        sleep(time_diff)
        pin.off()
        sleep(time_diff)


pin_cycle(status, 0.1, 2)
pin_cycle(boot, 0.1, 4)
pin_cycle(wifi, 0.1, 4)
pin_cycle(led_on, 0.1, 4)
pin_cycle(led_off, 0.1, 4)
