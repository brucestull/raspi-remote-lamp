from flask import Flask, redirect, url_for, jsonify
import RPi.GPIO as GPIO

app = Flask(__name__)

# BCM pin number for the lamp control:
lamp_control_pin = 17

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(lamp_control_pin, GPIO.OUT, initial=GPIO.LOW)

home_link = "<a href='/gpio/'>Home</a>"

form = """
	<form action="./on">
		<input type="submit" value="Pin 17 Up" />
	</form>
	<form action="./off">
		<input type="submit" value="Pin 17 Down" />
	</form>
"""


@app.route("/")
def home():
    return redirect(url_for("gpio_home"))


@app.route("/lamp-status/")
def lamp_status():
    lamp_pin_status_bin = GPIO.input(lamp_control_pin)
    if lamp_pin_status_bin == 0:
        lamp_pin_status_str = "OFF"
    elif lamp_pin_status_bin == 1:
        lamp_pin_status_str = "ON"
    else:
        lamp_pin_status_str = "UNKNOWN"
    data = {"lamp_pin_status": lamp_pin_status_str}
    return jsonify(data)


@app.route("/gpio/")
def gpio_home():
    return f"{home_link} <br> {form}"


@app.route("/gpio/on")
def gpio_on():
    GPIO.output(lamp_control_pin, GPIO.HIGH)
    return f"{home_link} <br> GPIO 17 turned on {form}"


@app.route("/gpio/off")
def gpio_off():
    GPIO.output(lamp_control_pin, GPIO.LOW)
    return f"{home_link} <br> GPIO 17 turned off {form}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
