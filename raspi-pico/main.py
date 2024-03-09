import network
import urequests
import json
from time import sleep
from machine import Pin
from picozero import pico_led


# Setup pin 18 as input:
pin18 = Pin(18, Pin.IN, Pin.PULL_DOWN)


# Function to fast-blink `pico_led`:
def pico_led_fast_blink(cycles):
    for _ in range(cycles):
        pico_led.on()
        sleep(.1)
        pico_led.off()
        sleep(.1)

# Function to load WiFi credentials from `config.json`:
def load_config(file_path):
    """
    Load a JSON configuration file and return it as a dictionary.
    """
    with open(file_path, "r") as f:
        config = json.load(f)
    return config


# Get the configuration settings from the config.json file:
config = load_config("config.json")
# Set the ssid and password from the configuration settings:
ssid = config["ssid"]
password = config["password"]
print("Loaded WiFi Settings!")


url_on = 'http://192.168.4.1:8000/gpio/on'
url_off = 'http://192.168.4.1:8000/gpio/off'

# Setup WiFi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection
while not wlan.isconnected():
    pass

print("Connected to WiFi!")
pico_led_fast_blink(10)


def handle_pin_change(pin):
    if pin.value() == 1:
        # Pin went high, turn on the LED
        print("Sending request to turn on LED")
        urequests.get(url_on).close()
        pico_led_fast_blink(5)
    else:
        # Pin went low, turn off the LED
        print("Sending request to turn off LED")
        urequests.get(url_off).close()
        pico_led.on()
        sleep(1)
        pico_led.off()

pin18.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=handle_pin_change)
