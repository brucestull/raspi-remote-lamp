# raspi_pico\main.py

import json
from time import sleep

import network
import urequests
from machine import Pin, reset
from picozero import pico_led

# Setup LED pins:
startup_led = Pin(20, Pin.OUT)
wifi_status_led = Pin(19, Pin.OUT)
lamp_on = Pin(18, Pin.OUT)
lamp_off = Pin(17, Pin.OUT)
shutdown_led = Pin(16, Pin.OUT)


# Setup input pins:
restart_button = Pin(15, Pin.IN, Pin.PULL_UP)
request_switch = Pin(14, Pin.IN, Pin.PULL_UP)


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


# Define a callback function to send the request:
def send_request(pin, off_route, on_route, off_pin, on_pin):
    """
    Function to send a request to the lamp server when the request switch is toggled.

    Args:
    pin (machine.Pin): The pin that triggered the interrupt.
    off_route (str): The route to the flask app to turn off the lamp.
    on_route (str): The route to the flask app to turn on the lamp.
    """
    if pin.value() == 0:
        # Pin went low, turn on the LED
        print(f"Sending request to turn on LED: {url_on}")
        urequests.get(on_route).close()
        led_blink(on_pin, 5)
    else:
        # Pin went high, turn off the LED
        print(f"Sending request to turn off LED: {url_off}")
        urequests.get(off_route).close()
        led_blink(off_pin, 2, 0.3)


def set_remote_lamp_to_switch_status(
    pin, led_function, off_route, on_route, off_pin, on_pin
):
    """
    Send initial request to the lamp server to set it to current switch status.

    Args:
    pin (machine.Pin): The pin that determines the current needed status of the lamp.
    led_function (function): The function to blink an LED.
    off_route (str): The route to the flask app to turn off the lamp.
    on_route (str): The route to the flask app to turn on the lamp.
    off_pin (machine.Pin): The pin to display the off status of the lamp.
    on_pin (machine.Pin): The pin to display the on status of the lamp.
    """
    if pin.value() == 0:
        # Pin is low, turn on the Lamp
        print("Pin is low, turning on the Lamp...")
        print(f"Sending request to turn on Lamp: {on_route}")
        urequests.get(on_route).close()
        led_function(on_pin, 5)
        return "Lamp should be ON!"
    else:
        # Pin is high, turn off the Lamp
        print("Pin is high, turning off the Lamp...")
        print(f"Sending request to turn off Lamp: {off_route}")
        urequests.get(off_route).close()
        led_function(off_pin, 5)
        return "Lamp should be OFF!"


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


# Set remote lamp to the current switch status and print the status:
lamp_switch_status = set_remote_lamp_to_switch_status(
    request_switch, led_blink, url_off, url_on, lamp_off, lamp_on
)
# Print the current Lamp switch status:
print(lamp_switch_status)


# Attach interrupt to Request-send pin:
request_switch.irq(
    trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
    handler=lambda pin: send_request(pin, url_off, url_on, lamp_off, lamp_on),
)
