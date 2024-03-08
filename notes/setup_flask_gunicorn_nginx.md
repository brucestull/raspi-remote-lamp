# Setup Flask Gunicorn Nginx

[Setup Flask Gunicorn Nginx - ChatGPT](https://chat.openai.com/share/433a0196-dcfc-447d-a3df-5d0ef9be1a46)

To set up a Flask application for production on a Raspberry Pi 4 running Raspberry Pi OS, you should use a more robust web server than the development server provided by Flask. A common production setup involves using Gunicorn as the WSGI server and Nginx as a reverse proxy to handle client requests efficiently. Here's how to set up your Flask app for production:

### 1. Install Gunicorn

First, you need to install Gunicorn. Gunicorn is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model, ported from Ruby's Unicorn project. Since you're likely using Python 3, you can install Gunicorn with pip:

```bash
pip3 install gunicorn
```

### 2. Test Gunicorn's Ability to Serve Your App

Before setting everything up, make sure Gunicorn can serve your Flask application. Navigate to your Flask application's directory and run:

```bash
gunicorn --workers 3 --bind 0.0.0.0:8000 myapp:app
```

Replace `myapp` with the name of the Python file that runs your Flask app (without the `.py` extension). If everything's set up correctly, you should be able to access your Flask app by going to `http://<Your-Raspberry-Pi-IP-Address>:8000/gpio/` from a web browser.

### 3. Install and Configure Nginx

Nginx is a high-performance HTTP server and reverse proxy. It can be used to handle requests to your server and then pass them to Gunicorn.

Install Nginx using apt:

```bash
sudo apt update
sudo apt install nginx
```

Once Nginx is installed, you need to configure it to forward requests to Gunicorn. You do this by editing (or creating) a server block configuration file within `/etc/nginx/sites-available/`. You can name this file after your project:

```bash
sudo nano /etc/nginx/sites-available/myapp
```

In this file, add the following configuration, adjusting it as necessary for your setup:

```nginx
server {
    listen 80;
    server_name <Your-Raspberry-Pi-IP-Address>;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Replace `<Your-Raspberry-Pi-IP-Address>` with your Raspberry Pi's IP address.

Enable the site by linking it to the `sites-enabled` directory:

```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
```

Test your Nginx configuration for syntax errors:

```bash
sudo nginx -t
```

If the test is successful, restart Nginx to apply the changes:

```bash
sudo systemctl restart nginx
```

### 4. Running Gunicorn as a System Service

To ensure Gunicorn continues to run in the background and starts automatically on boot, you can create a systemd service file:

```bash
sudo nano /etc/systemd/system/myapp.service
```

Add the following content, adjusting paths and names as necessary:

```ini
[Unit]
Description=Gunicorn instance to serve myapp
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=/home/pi/myapp
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind unix:myapp.sock -m 007 myapp:app

[Install]
WantedBy=multi-user.target
```

Replace `/home/pi/myapp` with the path to your Flask app. Then, start and enable the service:

```bash
sudo systemctl start myapp.service
sudo systemctl enable myapp.service
```

### 5. Adjust the Nginx Configuration to Use the Gunicorn Socket

Finally, update the Nginx configuration (`/etc/nginx/sites-available/myapp`) to use the Gunicorn socket:

```nginx
location / {
    proxy_pass http://unix:/home/pi/myapp/myapp.sock;
    include proxy_params;
}
```

Don’t forget to restart Nginx after making these changes:

```bash
sudo systemctl restart nginx
```

### Conclusion

Your Flask app should now be accessible through your Raspberry Pi's IP address without specifying a port, thanks to Nginx handling the incoming connections and passing them to Gunicorn, which in turn serves your Flask app. This setup is suitable for a production environment on your Raspberry Pi 4.
