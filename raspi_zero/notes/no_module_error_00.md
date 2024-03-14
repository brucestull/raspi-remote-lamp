# ModuleNotFoundError: No module named 'hardware_control'

[Flask App Testing: Mock Hardware - ChatGPT](https://chat.openai.com/share/2382b6f1-528a-4c50-a3f7-dd8596395c1d)

## Request

Help me understand what this error means and best practice ways to troubleshoot:

```powershell
PS C:\Users\FlynntKnapp\Programming\raspi-zero-lamp-server\raspi_zero> pytest
============================================== test session starts ===============================================
platform win32 -- Python 3.12.1, pytest-8.1.1, pluggy-1.4.0
rootdir: C:\Users\FlynntKnapp\Programming\raspi-zero-lamp-server\raspi_zero
plugins: flask-1.3.0
collected 0 items / 1 error

===================================================== ERRORS =====================================================
_______________________________________ ERROR collecting tests/test_app.py _______________________________________
ImportError while importing test module 'C:\Users\FlynntKnapp\Programming\raspi-zero-lamp-server\raspi_zero\tests\test_app.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests\test_app.py:7: in <module>
    from hardware_control import HardwareControl
E   ModuleNotFoundError: No module named 'hardware_control'
============================================ short test summary info =============================================
ERROR tests/test_app.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
================================================ 1 error in 0.17s ================================================
PS C:\Users\FlynntKnapp\Programming\raspi-zero-lamp-server\raspi_zero>
```

My directory structure:

```powershell
PS C:\Users\FlynntKnapp\Programming\raspi-zero-lamp-server\raspi_zero> tree /a /f
Folder PATH listing
Volume serial number is 40CB-1E6B
C:.
|   app.py
|   hardware_control.py
|   __init__.py
|
\---tests
        test_app.py
        __init__.py

PS C:\Users\FlynntKnapp\Programming\raspi-zero-lamp-server\raspi_zero>
```

The python modules:

```python
# raspi_zero\app.py

from flask import Flask, redirect, url_for, jsonify
import RPi.GPIO as GPIO
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
```

```python
# raspi_zero\hardware_control.py

import RPi.GPIO as GPIO


class HardwareControl:
    """
    A class to control the hardware of the Raspberry Pi Zero.

    Attributes:
        lamp_control_pin (int): The BCM pin number for the lamp control.
    """

    def __init__(self, lamp_control_pin):
        self.lamp_control_pin = lamp_control_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.lamp_control_pin, GPIO.OUT, initial=GPIO.LOW)

    def get_lamp_pin_status(self):
        """
        Get the status of the lamp pin.

        Returns:
            str: The status of the lamp pin.
        """
        lamp_pin_status_binary = GPIO.input(self.lamp_control_pin)
        if lamp_pin_status_binary == 0:
            return "OFF"
        elif lamp_pin_status_binary == 1:
            return "ON"
        else:
            return "UNKNOWN"
        # Alternate implementation:
        # if lamp_pin_status_binary == 0:
        #     lamp_pin_status_str = "OFF"
        # elif lamp_pin_status_binary == 1:
        #     lamp_pin_status_str = "ON"
        # else:
        #     lamp_pin_status_str = "UNKNOWN"
        # return lamp_pin_status_str

    def turn_lamp_on(self):
        """
        Turn the lamp on.
        """
        GPIO.output(self.lamp_control_pin, GPIO.HIGH)
        return "Lamp turned on."

    def turn_lamp_off(self):
        """
        Turn the lamp off.
        """
        GPIO.output(self.lamp_control_pin, GPIO.LOW)
        return "Lamp turned off."
```

```python
# raspi_zero\tests\test_app.py

import json
from unittest.mock import patch


import pytest
from unittest.mock import patch
from hardware_control import HardwareControl


@pytest.fixture
def gpio_mock(mocker):
    """
    Fixture to mock the RPi.GPIO module.
    """
    mock = mocker.patch("your_flask_app_module.RPi.GPIO")
    return mock


def test_turn_lamp_on(gpio_mock):
    """
    Test the turn_lamp_on method.
    """
    lamp_control_pin = 17  # Example pin number
    hc = HardwareControl(lamp_control_pin)
    hc.turn_lamp_on()
    gpio_mock.output.assert_called_once_with(lamp_control_pin, gpio_mock.HIGH)


def test_turn_lamp_off(gpio_mock):
    """
    Test the turn_lamp_off method.
    """
    lamp_control_pin = 17  # Example pin number
    hc = HardwareControl(lamp_control_pin)
    hc.turn_lamp_off()
    gpio_mock.output.assert_called_once_with(lamp_control_pin, gpio_mock.LOW)


def test_get_lamp_pin_status(gpio_mock):
    """
    Test the get_lamp_pin_status method.
    """
    lamp_control_pin = 17  # Example pin number
    hc = HardwareControl(lamp_control_pin)
    # Simulate lamp is on
    gpio_mock.input.return_value = 1
    assert hc.get_lamp_pin_status() == "ON"
    # Simulate lamp is off
    gpio_mock.input.return_value = 0
    assert hc.get_lamp_pin_status() == "OFF"


def test_home_redirect(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/gpio/" in response.location


def test_gpio_home(client):
    response = client.get("/gpio/")
    assert response.status_code == 200
    assert "Pin 17 Up" in response.data.decode()


@patch(
    "raspi_zero.hardware_control.HardwareControl.get_lamp_status", return_value="OFF"
)
def test_lamp_status_off(mock_get_lamp_status, client):
    response = client.get("/lamp-status/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["lamp_pin_status"] == "OFF"


@patch("raspi_zero.hardware_control.HardwareControl.get_lamp_status", return_value="ON")
def test_lamp_status_on(mock_get_lamp_status, client):
    response = client.get("/lamp-status/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["lamp_pin_status"] == "ON"
```

Please walk me through what the error actually means. Please try to provide alternate ways to explain. I want to be a better troubleshooter of my code.

### Response

The error message you encountered during the pytest session is a `ModuleNotFoundError`, specifically stating: `No module named 'hardware_control'`. This error indicates that Python is unable to locate the module `hardware_control.py` when trying to import it in your test module `test_app.py`. Understanding why this happens and knowing how to troubleshoot such issues are essential skills for a developer. Here's a breakdown of the error and how to approach solving it:

### Understanding the Error

1. **Error Context**: The error occurred when pytest attempted to collect tests from the file `tests/test_app.py`. During the import phase of this file, it tried to import `HardwareControl` from a module named `hardware_control` but failed.

2. **Python's Import System**: Python uses a system of paths to locate modules. When you import a module, Python searches through the directories listed in `sys.path` to find the module. If the module's directory is not in `sys.path`, Python will not find it, leading to a `ModuleNotFoundError`.

3. **Test Environment**: Tests often run in a slightly different environment than the main application, especially regarding the current working directory and the Python path. When running pytest, it might not automatically include the root directory of your project (where `hardware_control.py` is located) in its path.

### Troubleshooting Steps

#### 1. Check `__init__.py` Files
You already have `__init__.py` files in place, which is good because they signal to Python that these directories should be treated as packages. However, the problem is not with package recognition in this case.

#### 2. Verify the Import Path
Make sure that the way you're trying to import `HardwareControl` matches the directory structure. From your test file's perspective, an import from `hardware_control` assumes that `hardware_control.py` is in the same directory or in one of the directories listed in `sys.path`.

#### 3. Adjusting `sys.path` or Using Absolute Imports
There are a couple of ways to address the path issue:

- **Adjust `sys.path`**: You can add the root directory of your project (`raspi_zero`) to `sys.path` at the beginning of your test files. However, this is generally considered a less favorable solution as it can make your tests less portable and harder to understand.
  
  ```python
  import sys
  sys.path.append('/path/to/raspi_zero')
  from hardware_control import HardwareControl
  ```

- **Use a src Directory**: A better practice is to structure your project with a `src` directory. You would move your application code into `src`, and then use setuptools or a similar tool to install your application package in editable mode (`pip install -e .`). This way, your module would be correctly located by Python's import system, both when running the app and the tests.

#### 4. Running Pytest with the Correct Working Directory
Ensure you run pytest from the root directory of your project (`raspi_zero`). Running it from a subdirectory might cause Python to not find the module.

#### 5. Using Pytest's PYTHONPATH Modification
Pytest offers a way to modify `PYTHONPATH` directly from the pytest.ini configuration file, ensuring that your project root is included. You can create a `pytest.ini` file in your project root with the following content:

```ini
[pytest]
python_paths = .
```

This tells pytest to include the current directory (project root) in `PYTHONPATH`, ensuring your imports can be resolved correctly.

### Conclusion
The best practice for avoiding such issues involves ensuring a clear and Pythonic project structure, making good use of virtual environments, and understanding how Python's import system works. Structuring your project with a `src` directory and installing your project in editable mode can help make your imports more predictable and your project more maintainable.