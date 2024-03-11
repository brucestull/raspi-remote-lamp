# Start Flask App on Boot

[Start Flask App on Boot - ChatGPT](https://chat.openai.com/share/ebd2a89d-e33b-47c3-8463-e072ebc186ba)

## Request

I have a flask app at `/path/to/flask.py`. The computer is linux ubuntu server.

How do I starte `/path/to/flask.py` on system startup?

### Answer

Starting a Flask application on system startup on an Ubuntu server can be achieved using systemd. systemd is a system and service manager for Linux operating systems which allows you to create a service file for your application. This service will be managed by systemd and can be configured to start automatically at system boot.

Here's a step-by-step guide to achieve this:

### 1. Create a systemd Service File

You'll first need to create a service file for your Flask application. This file will tell systemd how to start and manage your application.

1. **Open a new service file in a text editor** with sudo privileges. We'll name the service `flaskapp.service` but you can name it whatever you like:

```bash
sudo nano /etc/systemd/system/flaskapp.service
```

2. **Add the following content** to the file, adjusting the `ExecStart`, `WorkingDirectory`, `User`, and other fields as necessary for your specific application:

```ini
[Unit]
Description=Flask application
After=network.target

[Service]
User=<username>
Group=<usergroup>
WorkingDirectory=/path/to
ExecStart=/path/to/your/python /path/to/flask.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Replace `<username>` and `<usergroup>` with the username and group under which you want the application to run, and `/path/to/your/python` with the path to the Python interpreter you're using (you can find this with `which python3`).

### 2. Reload systemd Daemon

After creating the service file, you need to reload the systemd daemon to recognize the new service:

```bash
sudo systemctl daemon-reload
```

### 3. Enable and Start Your Flask Service

To have your Flask application start on boot, enable the service:

```bash
sudo systemctl enable flaskapp.service
```

Then, start the service immediately:

```bash
sudo systemctl start flaskapp.service
```

### 4. Verify the Service Status

You can check the status of your service to ensure it's running as expected:

```bash
sudo systemctl status flaskapp.service
```

### Additional Notes

- This guide assumes you have a working Flask application and you are familiar with basic Linux and terminal operations.
- Ensure your Flask application is executable and has the correct shebang (e.g., `#!/usr/bin/env python3`) at the top of the file if you're executing it directly.
- Adjust the service file according to your Flask app's specific requirements, such as environment variables or additional dependencies.

This setup should allow your Flask application to start automatically when your Ubuntu server boots up, making it easier to manage and deploy.