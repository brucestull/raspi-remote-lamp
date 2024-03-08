# Raspberry Pi 4 - Flask - Pin 17

Flask app to control GPIO pin 17 from remote web browser.

## Server

[Remote GPIO Control with Flask - ChatGPT](https://chat.openai.com/share/dc7c5899-53cf-4450-bf2e-5d31dfa1d37c)

I have a raspberry Pi 4 B running raspberry pi OS. It has the GPIO header installed. How can I have a computer on my local network send an http request to the raspberry pi to turn on GPIO pin 17?

### Response

To control GPIO pins on your Raspberry Pi 4 using HTTP requests, you can set up a simple web server on your Raspberry Pi that listens for incoming requests and then triggers GPIO operations based on those requests. Here's a step-by-step guide to achieve this:

1. **Install Flask**:
   Flask is a lightweight Python web framework. You can install it using pip:

   ```
   sudo pip install flask
   ```

2. **Write the Flask Server Code**:
   Create a Python script (let's name it `gpio_server.py`) with the following content:

   ```python
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
   ```

   This script sets up a Flask web server listening on port 80. It defines two routes `/gpio/on` and `/gpio/off` to turn GPIO 17 on and off respectively.

3. **Run the Flask Server**:
   Execute the Flask server script:

   ```
   sudo python gpio_server.py
   ```

4. **Sending HTTP Requests from Another Computer**:
   You can send HTTP requests from another computer on the same local network to control GPIO 17 on the Raspberry Pi.

   To turn on GPIO 17, send a GET request to `http://raspberrypi.local/gpio/on` (replace `raspberrypi` with your Raspberry Pi's hostname or IP address).

   To turn off GPIO 17, send a GET request to `http://raspberrypi.local/gpio/off`.

Make sure your Raspberry Pi and the computer sending requests are on the same local network. Additionally, ensure that your Raspberry Pi's firewall or any network-level restrictions allow incoming HTTP traffic on port 80.

Remember, controlling GPIO pins remotely over HTTP can have security implications, so ensure proper authentication and authorization mechanisms if deploying in a production environment.

## Client

[Python Script HTTP Request - ChatGPT](https://chat.openai.com/share/0eb8c54c-4ffd-4ffa-9c27-a6a38cd2a538)

Help me write a python script to send an http request to `192.168.1.181/gpio/off`?

### Response


Certainly! You can use the `requests` library in Python to send HTTP requests. Here's a simple script to send a GET request to `192.168.1.181/gpio/off`:

```python
import requests

def send_http_request():
    url = 'http://192.168.1.181/gpio/off'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("HTTP request sent successfully.")
        else:
            print(f"Failed to send HTTP request. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_http_request()
```

Make sure you have the `requests` library installed in your 
