from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)

home = "<a href='/gpio/'>Home</a>"

form = """
	<form action="./on">
		<input type="submit" value="Pin 17 Up" />
	</form>
	<form action="./off">
		<input type="submit" value="Pin 17 Down" />
	</form>
"""

@app.route('/gpio/')
def gpio_home():
    return home + "<br>" + form

@app.route('/gpio/on')
def gpio_on():
    GPIO.output(17, GPIO.HIGH)
    return (
	f"{home}"
	f"<br>"
	f"GPIO 17 turned on"
        f"{form}"
    )

@app.route('/gpio/off')
def gpio_off():
    GPIO.output(17, GPIO.LOW)
    return (
	f"{home}"
	f"<br>"
	f"GPIO 17 turned off"
	f"{form}"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)



