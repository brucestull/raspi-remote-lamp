# Flask Testing with Pytest

[Flask Testing with Pytest - ChatGPT](https://chat.openai.com/share/a02472d6-7b5b-4cec-baab-37dc3e7f2051)

## Request

I have a flask app. Please help me write tests for it using `pytest`?

```python
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
```

## Response

Testing a Flask application involves several steps, including setting up a test configuration, using the Flask test client, and mocking external services or libraries—in this case, the `RPi.GPIO` library. The `pytest` framework, along with the `unittest.mock` module for mocking, can be used effectively to test your Flask app.

### 1. Install Testing Libraries
First, ensure you have `pytest` and `pytest-flask` installed. If you haven't installed these yet, you can do so using pip:

```sh
pip install pytest pytest-flask
```

### 2. Configure Pytest for Flask
Create a file named `conftest.py` in your tests directory (create a `tests` directory if you don't have one). This file is used by pytest to share fixtures across multiple test files.

```python
import pytest
from your_flask_app_file import app  # Adjust the import path as necessary

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
```

Replace `your_flask_app_file` with the name of your Python file containing the Flask app, e.g., `app.py`.

### 3. Mock the GPIO Library
Before you start writing tests, it's crucial to mock the `RPi.GPIO` library to prevent your tests from attempting to access GPIO hardware directly.

In your tests, you can use the `unittest.mock.patch` decorator to mock the GPIO module. Here's an example of how you might mock the GPIO setup and input/output functions:

```python
from unittest.mock import patch
```

### 4. Writing Tests
Now, let's write some tests. Create a new test file in your tests directory, e.g., `test_app.py`. Here's an example of how your tests might look:

```python
import json
from unittest.mock import patch

def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/gpio/' in response.location

def test_gpio_home(client):
    response = client.get('/gpio/')
    assert response.status_code == 200
    assert 'Pin 17 Up' in response.data.decode()

@patch('your_flask_app_file.GPIO.input', return_value=0)
def test_lamp_status_off(mock_gpio_input, client):
    response = client.get('/lamp-status/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['lamp_pin_status'] == 'OFF'

@patch('your_flask_app_file.GPIO.input', return_value=1)
def test_lamp_status_on(mock_gpio_input, client):
    response = client.get('/lamp-status/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['lamp_pin_status'] == 'ON'
```

### 5. Running Tests
To run your tests, use the `pytest` command in your terminal. Pytest will automatically discover and run tests in files named `test_*.py` or `*_test.py`.

### Tips:
- Replace `your_flask_app_file` with the actual name of your Flask app file.
- Use `@patch` to mock `RPi.GPIO` functions as needed in different test cases, depending on whether you're testing the ON or OFF states or other behaviors.
- If your Flask app grows, consider organizing tests into classes or separate files for different aspects of the app.

This setup gives you a basic structure for testing your Flask application and mocking hardware interactions. You can extend it with more tests as needed to cover other functionalities or edge cases in your application.
