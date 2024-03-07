from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)

@app.route('/gpio/on')
def gpio_on():
    GPIO.output(17, GPIO.HIGH)
    return 'GPIO 17 turned on'

@app.route('/gpio/off')
def gpio_off():
    GPIO.output(17, GPIO.LOW)
    return 'GPIO 17 turned off'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
