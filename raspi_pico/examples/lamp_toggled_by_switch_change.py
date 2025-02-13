# raspi_pico\main.py

import json
from time import sleep

import network
import urequests
from machine import Pin, reset

# Setup LED pins:
startup_led = Pin(20, Pin.OUT)
wifi_status_led = Pin(19, Pin.OUT)
lamp_on_led = Pin(18, Pin.OUT)
lamp_off_led = Pin(17, Pin.OUT)
shutdown_led = Pin(16, Pin.OUT)


# Setup input pins:
restart_button = Pin(15, Pin.IN, Pin.PULL_UP)
request_switch = Pin(14, Pin.IN, Pin.PULL_DOWN)


# Function to blink `led`:
def led_blink(led, cycles=2, time_diff=0.1):
    """
    Blink the LED `led` for `cycles` times with a time difference of `time_diff` seconds.

    Args:
    led (machine.Pin): The LED pin to blink.
    cycles (int): The number of times to blink the LED.
    time_diff (float): The time difference between LED on and off states.
    """
    for _ in range(cycles):
        led.on()
        sleep(time_diff)
        led.off()
        sleep(time_diff)


# Define a callback function to reset the Pico:
def restart_pico(led_blink_function, led, cycles=4, time_diff=0.1):
    """
    Restart the Pico when the restart button is pressed.
    This version allows passing a custom `led_blink_function` and its parameters.

    Args:
    led_blink_function (function): The function to blink an LED.
    led (Pin): The LED pin to blink.
    cycles (int): The number of times to blink the LED (default is 4).
    time_diff (float): The time difference between LED on and off states (default is 0.1 seconds).
    """
    print("We're trying to restart this thing...")
    led_blink_function(led, cycles, time_diff)
    sleep(0.5)
    reset()


def send_request(request_route, led_pin):
    """
    Send a request to to lamp endpoint `request_route` and blink led on pin `led_pin`.

    Args:
    toggle_route (str): The route to the flask app to toggle the lamp.
    on_led_pin (machine.Pin): The pin to display the toggle status of the lamp.
    """
    print(f"Sending request to toggle LED: {url_toggle}")
    led_blink(led_pin, 5)
    urequests.get(request_route).close()


# Attach interrupt to Restart button pin:
restart_button.irq(
    trigger=Pin.IRQ_FALLING,
    handler=lambda pin: restart_pico(led_blink, shutdown_led, 6),
)


# Blink LED to indicate startup:
led_blink(startup_led, 3)


# Function to load WiFi credentials from `file_path`:
def load_config(file_path):
    """
    Load a JSON configuration file and return it as a dictionary.
    """
    with open(file_path, "r") as f:
        config = json.load(f)
    return config


# Get the configuration settings from the `config.json` file:
config = load_config("config.json")
# Set the ssid and password from the configuration settings:
ssid = config["ssid"]
password = config["password"]
print("Loaded WiFi Settings!")

# Get the lamp host from the configuration settings:
lamp_host = config["lamp_host"]

# Define the URLs for the lamp control:
url_on = f"{lamp_host}/gpio/on"
url_off = f"{lamp_host}/gpio/off"
url_toggle = f"{lamp_host}/gpio/toggle"

# Setup WiFi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection
while not wlan.isconnected():
    pass

print("Connected to WiFi!")
led_blink(wifi_status_led, 10)
# Turn on `wifi_status_led` to indicate successful connection to WiFi:
wifi_status_led.on()


# The `pin` argument is passed automatically by the `irq` method even though it's not
# used in the lambda function.
request_switch.irq(
    trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
    handler=lambda pin: send_request(url_toggle, lamp_on_led),
)
