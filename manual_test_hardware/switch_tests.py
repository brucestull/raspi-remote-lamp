# test_modules\switch_tests.py

from time import sleep

from machine import Pin
from picozero import pico_led


def pin_cycle(pin, time_diff, cycles):
    for _ in range(cycles):
        pin.on()
        sleep(time_diff)
        pin.off()
        sleep(time_diff)


# Blink the pico_led so we know the thing's starting up:
pin_cycle(pico_led, 0.08, 6)

# Set pins for `reset_button` and `control_switch`:
reset_button = Pin(15, Pin.IN, Pin.PULL_UP)
control_switch = Pin(14, Pin.IN, Pin.PULL_UP)


def control_handler(pin, time_diff=0.1, cycles=2):
    for _ in range(cycles):
        pin.on()
        sleep(time_diff)
        pin.off()
        sleep(time_diff)


reset_button.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: control_handler(pico_led))
control_switch.irq(
    trigger=Pin.IRQ_FALLING, handler=lambda pin: control_handler(pico_led)
)
