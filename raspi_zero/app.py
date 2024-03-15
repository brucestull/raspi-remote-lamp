# raspi_zero\app.py

from flask import Flask, jsonify, redirect, url_for

from hardware_control import HardwareControl

app = Flask(__name__)

# BCM pin number for the lamp control:
lamp_control_pin = 17

# Initialize the hardware control:
hardware = HardwareControl(lamp_control_pin)

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
    lamp_pin_status_str = hardware.get_lamp_pin_status()
    data = {"lamp_pin_status": lamp_pin_status_str}
    return jsonify(data)


@app.route("/gpio/")
def gpio_home():
    lamp_pin_status_str = hardware.get_lamp_pin_status()
    return f"{home_link} <br> Lamp is: {lamp_pin_status_str} {form}"


@app.route("/gpio/on")
def gpio_on():
    response = hardware.turn_lamp_on()
    return f"{home_link} <br> {response} {form}"


@app.route("/gpio/off")
def gpio_off():
    response = hardware.turn_lamp_off()
    return f"{home_link} <br> {response} {form}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
