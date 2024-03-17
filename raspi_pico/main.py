# raspi_pico\main.py

import json
from time import sleep

import network
import urequests
from machine import Pin, reset
from picozero import pico_led

# Setup LED pins:
restart_status_led = Pin(16, Pin.OUT)
wifi_status_led = Pin(17, Pin.OUT)
lamp_on = Pin(18, Pin.OUT)
lamp_off = Pin(19, Pin.OUT)


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


# Function to load WiFi credentials from `config.json`:
def load_config(file_path):
    """
    Load a JSON configuration file and return it as a dictionary.
    """
    with open(file_path, "r") as f:
        config = json.load(f)
    return config


# Setup input pins:
restart_button = Pin(15, Pin.IN, Pin.PULL_UP)
# Setup pin 18 (Request-send pin) as input:
request_switch = Pin(14, Pin.IN, Pin.PULL_UP)


# Attach interrupt to Restart pin:
restart_button.irq(
    trigger=Pin.IRQ_FALLING,
    handler=lambda pin: restart_pico(led_blink, restart_status_led, 6),
)

# Setup pin 18 (Request-send pin) as input:
request_switch = Pin(14, Pin.IN, Pin.PULL_UP)


# Blink LED to indicate startup:
led_blink(restart_status_led, 3)

# Get the configuration settings from the config.json file:
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


# Define a callback function to send the request:
def send_request(pin):
    if pin.value() == 0:
        # Pin went low, turn on the LED
        print(f"Sending request to turn on LED: {url_on}")
        urequests.get(url_on).close()
        led_blink(lamp_on, 5)
    else:
        # Pin went high, turn off the LED
        print(f"Sending request to turn off LED: {url_off}")
        urequests.get(url_off).close()
        led_blink(lamp_off, 2, 0.3)


# Attach interrupt to Request-send pin:
request_switch.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=send_request)
