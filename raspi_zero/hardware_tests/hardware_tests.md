# Hardware Tests

# Read Raspi Pico GPIO

[Read Raspi Pico GPIO - ChatGPT](https://chat.openai.com/share/29261a72-e3da-4218-945e-fd0cfe66e254)

## Request

I have a Raspi Pico. How do I read the current state of input gpio pin 14?

## Response

To read the current state of GPIO pin 14 on a Raspberry Pi Pico using MicroPython, you'll need to follow these steps. This assumes you have MicroPython installed on your Raspberry Pi Pico. If you haven't set up MicroPython yet, you'll need to do that first by following the official Raspberry Pi Pico/MicroPython setup guide.

Here's how you can read the state of GPIO pin 14:

1. **Connect to Your Raspberry Pi Pico**: Use a program like Thonny or minicom to connect to your Raspberry Pi Pico. This will give you access to the MicroPython REPL (Read-Eval-Print Loop), where you can execute MicroPython commands directly on the Pico.

2. **Import Required Library**: At the prompt, import the `Pin` class from the `machine` module. This module provides functions related to the hardware, including GPIO pins.

    ```python
    from machine import Pin
    ```

3. **Initialize the Pin**: Initialize pin 14 as an input. This tells the Raspberry Pi Pico that you want to read the state of this pin.

    ```python
    pin14 = Pin(14, Pin.IN)
    ```

4. **Read the Pin State**: Now, you can read the current state of pin 14. The `value()` method will return `0` if the pin is low (0V) and `1` if the pin is high (3.3V).

    ```python
    state = pin14.value()
    print(state)
    ```

If `state` prints `0`, the pin is in a low state; if it prints `1`, the pin is in a high state.

Remember, the physical setup of your Raspberry Pi Pico and the devices or sensors connected to GPIO pin 14 may affect the way you read or interpret the pin's state. For example, if you have a switch connected to GPIO pin 14 and ground (GND), pressing the switch would bring the pin to a low state (0), and releasing it would return it to a high state (1) if you have a pull-up resistor configured either externally or internally.
