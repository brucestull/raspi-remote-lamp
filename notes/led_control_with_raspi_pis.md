# LED Control with Raspberry Pis

[LED Control with Raspberry Pis - ChatGPT](https://chat.openai.com/share/90e11f99-6f6c-49cc-bc37-d89b0fb94309)

## Request

I'm using a raspi pico w to send http requests to control an led on a raspi zero w. That works like I expect. 

What is a best practice way, in the pico, to check the status of pin 18, if it's high send the http request to turn on the led, if pin 18 is low send http request to turn off the led?

### Response

To efficiently use a Raspberry Pi Pico W to control an LED on a Raspberry Pi Zero W via HTTP requests based on the status of pin 18, you'll need to employ a polling or interrupt-based method on the Pico to check the state of pin 18 and then use its Wi-Fi capabilities to send the appropriate HTTP request.

Here's a general approach for a best practice implementation:

### 1. Setup the Raspberry Pi Pico W

You will use MicroPython for programming the Pico W. Ensure you have the latest version of MicroPython that supports the Pico W's Wi-Fi capabilities.

#### Initialization

- Initialize pin 18 as an input with pull-up or pull-down depending on your circuit.
- Initialize the Wi-Fi connection.

#### Code Sample

```python
from machine import Pin
import network
import urequests

# Setup pin 18 as input
pin18 = Pin(18, Pin.IN, Pin.PULL_DOWN)

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('your_ssid', 'your_password')

# Check if connected to Wi-Fi
while not wlan.isconnected():
    pass
```

### 2. Polling or Interrupt for Pin Status

#### Polling Method

You continuously check the status of pin 18 in a loop and send HTTP requests based on its state. This method is simpler but less efficient, as it continuously occupies the CPU.

```python
def check_pin_and_send_request():
    previous_state = None
    while True:
        current_state = pin18.value()
        if current_state != previous_state:
            if current_state == 1:
                # Pin is high, turn on the LED
                response = urequests.get('http://raspi-zero-w-address/led/on')
            else:
                # Pin is low, turn off the LED
                response = urequests.get('http://raspi-zero-w-address/led/off')
            previous_state = current_state
            response.close()
```

#### Interrupt Method

An interrupt-based approach is more efficient as it triggers code execution in response to a pin state change without continuous polling.

```python
def handle_pin_change(pin):
    if pin.value() == 1:
        # Pin went high, turn on the LED
        urequests.get('http://raspi-zero-w-address/led/on').close()
    else:
        # Pin went low, turn off the LED
        urequests.get('http://raspi-zero-w-address/led/off').close()

pin18.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=handle_pin_change)
```

### 3. Flask Server on Raspberry Pi Zero W

On the Raspberry Pi Zero W, ensure you have a Flask server running to listen for the HTTP requests to control the LED.

#### Flask App Example

```python
from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)

LED_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

@app.route('/led/<state>')
def led_control(state):
    if state == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
    elif state == "off":
        GPIO.output(LED_PIN, GPIO.LOW)
    return f"LED {state}"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```

This code outlines the basic logic. Remember to replace placeholder values with your actual Wi-Fi credentials, Raspberry Pi Zero W's IP address, and adjust the pin numbers as per your setup. This approach ensures efficient use of the Raspberry Pi Pico W's capabilities while maintaining simplicity in controlling an external device over the network.
