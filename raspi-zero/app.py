from flask import Flask, redirect, url_for, jsonify
from raspi_zero.hardware_control import HardwareControl

# Create a Flask app
app = Flask(__name__)

# Create an instance of HardwareControl
hardware_control = HardwareControl()

# BCM pin number for the lamp control:
lamp_control_pin = 17

# Set up hardware_control
hardware_control.setmode(hardware_control.BCM)
hardware_control.setup(
    lamp_control_pin, hardware_control.OUT, initial=hardware_control.LOW
)

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
    lamp_pin_status_bin = hardware_control.get_lamp_status()
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
    hardware_control.turn_on_lamp()
    return f"{home_link} <br> GPIO 17 turned on {form}"


@app.route("/gpio/off")
def gpio_off():
    hardware_control.turn_off_lamp()
    return f"{home_link} <br> GPIO 17 turned off {form}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
