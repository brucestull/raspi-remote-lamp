from flask import Flask, jsonify, redirect, url_for
from hardware_control import HardwareControl

app = Flask(__name__)

# BCM pin number for the lamp control:
lamp_control_pin = 24

# Initialize the hardware control:
hardware = HardwareControl(lamp_control_pin)

lamp_status_url = "/lamp-status/"
gpio_home_url = "/gpio/"
gpio_on_url = "/gpio/on"
gpio_off_url = "/gpio/off"
gpio_toggle_url = "/gpio/toggle"

home_link = f"<a href='{gpio_home_url}'>Home</a>"

def form_builder(url, text, pin=lamp_control_pin):
	return f"""
	<form action='{url}'>
		<input type="submit" value="{text} pin {pin}, please?" />
	</form>
"""

toggle_form = form_builder(gpio_toggle_url, "Toggle")
on_form = form_builder(gpio_on_url, "Turn ON")
off_form = form_builder(gpio_off_url, "Turn OFF")

form = toggle_form + on_form + off_form


@app.route("/")
def home():
    return redirect(url_for("gpio_home"))


@app.route(lamp_status_url)
def lamp_status():
    lamp_pin_status_str = hardware.get_lamp_pin_status()
    data = {"lamp_pin_status": lamp_pin_status_str}
    return jsonify(data)


@app.route(gpio_home_url)
def gpio_home():
    lamp_pin_status_str = hardware.get_lamp_pin_status()
    return f"{home_link} <br> Lamp is: {lamp_pin_status_str} {form}"


@app.route(gpio_on_url)
def gpio_on():
    response = hardware.turn_lamp_on()
    return f"{home_link} <br> {response} {form}"


@app.route(gpio_off_url)
def gpio_off():
    response = hardware.turn_lamp_off()
    return f"{home_link} <br> {response} {form}"


@app.route(gpio_toggle_url)
def gpio_toggle():
    status = hardware.toggle_lamp()
    print(status)
    return redirect(url_for("gpio_home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
