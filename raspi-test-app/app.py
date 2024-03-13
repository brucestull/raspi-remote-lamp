# app.py
from flask import Flask
from hardware_control import HardwareControl

app = Flask(__name__)
hardware_control = HardwareControl()


@app.route("/gpio/17/on")
def turn_on_17():
    hardware_control.turn_on_relay(17)
    return "Relay on BCM pin 17 turned on"


@app.route("/gpio/18/off")
def turn_off_18():
    hardware_control.turn_off_relay(18)
    return "Relay on BCM pin 18 turned off"


if __name__ == "__main__":
    app.run(debug=True)
