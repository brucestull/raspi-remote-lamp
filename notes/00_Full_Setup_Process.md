
Awesome project. Here’s a clean, reproducible way to stand up your “remote lamp server” on a Pi Zero (W / 2 W), using a proper Python virtualenv, Gunicorn, and Nginx, plus a built-in Wi-Fi access point your Pico can join.

---

# 0) One-time OS prep (after first boot & updates)

```bash
# 0.1 – Base tooling & GPIO libs
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y python3-venv python3-pip git nginx \
                    python3-rpi.gpio  # gives RPi.GPIO via apt (no building)

# 0.2 – Set Wi-Fi country (required for AP mode)
sudo raspi-config nonint do_wifi_country US

# 0.3 – Create a dedicated app user with least privileges
sudo adduser --system --group --home /srv/lamp lampapp
# allow non-root access to GPIO memory
sudo usermod -aG gpio lampapp
```

> Why `python3-rpi.gpio` from apt? On older ARM (Pi Zero), compiling GPIO wheels can be finicky. Using the distro package “just works.” We’ll give the venv access to system packages.

---

# 1) App layout & virtual environment

```bash
# 1.1 – Put your app in /srv/lamp
sudo mkdir -p /srv/lamp
sudo chown -R lampapp:lampapp /srv/lamp

# 1.2 – copy your code in (app.py + hardware_control.py, etc.)
# If you’ll git-clone:
# sudo -u lampapp git clone <your-repo> /srv/lamp

# 1.3 – venv (with system site-packages so apt GPIO lib is visible)
sudo -u lampapp python3 -m venv --system-site-packages /srv/lamp/venv
sudo -u lampapp /srv/lamp/venv/bin/pip install --upgrade pip
sudo -u lampapp /srv/lamp/venv/bin/pip install flask gunicorn
```

Optional (nice to have): add a tiny `wsgi.py` so Gunicorn always imports the same symbol.

```bash
cat <<'PY' | sudo tee /srv/lamp/wsgi.py
from app import app  # your app.py defines "app = Flask(__name__)"
PY
sudo chown lampapp:lampapp /srv/lamp/wsgi.py
```

> Run test locally once:

```bash
sudo -u lampapp /srv/lamp/venv/bin/python -c "import app; print('OK, found', app.app)"
```

---

# 2) Production server: Gunicorn (app) + Nginx (front)

* **Nginx** sits in front as a reverse proxy. It terminates HTTP(S), serves static files efficiently, manages keep-alives, request buffering, and can do retries/rate-limits/TLS later.
* **Gunicorn** runs your Flask app as a robust, multi-process WSGI server.

## 2.1 Gunicorn systemd unit

```bash
sudo tee /etc/systemd/system/gunicorn-lamp.service >/dev/null <<'UNIT'
[Unit]
Description=Gunicorn for Lamp Flask app
After=network-online.target
Wants=network-online.target

[Service]
User=lampapp
Group=www-data
WorkingDirectory=/srv/lamp
Environment=PYTHONUNBUFFERED=1
# Create /run/gunicorn-lamp/ for the socket
RuntimeDirectory=gunicorn-lamp
RuntimeDirectoryMode=0755
ExecStart=/srv/lamp/venv/bin/gunicorn --workers 1 --threads 2 \
          --bind unix:/run/gunicorn-lamp/socket wsgi:app
Restart=always
# GPIO access without root (thanks to group membership)
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
UNIT

sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn-lamp
sudo systemctl status gunicorn-lamp --no-pager
```

> Pi Zero is single-core; `--workers 1 --threads 2` is a good starting point. Bump threads to 4 only if needed.

## 2.2 Nginx site

```bash
sudo tee /etc/nginx/sites-available/lamp >/dev/null <<'NGINX'
server {
    listen 80 default_server;
    server_name _;

    access_log /var/log/nginx/lamp_access.log;
    error_log  /var/log/nginx/lamp_error.log;

    location / {
        proxy_pass http://unix:/run/gunicorn-lamp/socket;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect off;
    }
}
NGINX

sudo ln -s /etc/nginx/sites-available/lamp /etc/nginx/sites-enabled/lamp
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx
```

Smoke test on the Pi:

```bash
curl -i http://127.0.0.1/    # should 302 -> /gpio/
curl -s http://127.0.0.1/lamp-status/ | jq
```

---

# 3) Start on boot

* You already enabled Gunicorn and Nginx services. They’ll start automatically at boot.
* Your Flask app logs are visible with:

```bash
journalctl -u gunicorn-lamp -f
```

---

# 4) Built-in Wi-Fi Access Point for the Pico

**Best-practice on Raspberry Pi OS Bookworm:** use **NetworkManager** (default) to create a persistent AP; it handles DHCP and NAT automatically. This is lighter and simpler than juggling `hostapd` + `dnsmasq`.

Decide your AP LAN: `192.168.50.0/24`
Pi AP IP: `192.168.50.1` (the Pico will call `http://192.168.50.1/gpio/toggle`)

```bash
# Make sure NetworkManager controls wlan0 (default on Bookworm)
nmcli dev status

# Create a persistent AP connection
sudo nmcli connection add type wifi ifname wlan0 con-name lamp-ap ssid LampAP
sudo nmcli connection modify lamp-ap 802-11-wireless.mode ap 802-11-wireless.band bg
sudo nmcli connection modify lamp-ap wifi-sec.key-mgmt wpa-psk wifi-sec.psk "ChangeMe-StrongPass!"

# Give the AP interface a stable address and hand out DHCP via "shared"
sudo nmcli connection modify lamp-ap ipv4.method shared ipv4.addresses 192.168.50.1/24
sudo nmcli connection modify lamp-ap ipv6.method ignore
sudo nmcli connection up lamp-ap
```

Keep it always on:

```bash
sudo nmcli connection modify lamp-ap connection.autoconnect yes
```

**Disable Wi-Fi power save** (helps keep the AP stable):

```bash
sudo tee /etc/NetworkManager/conf.d/wifi-powersave.conf >/dev/null <<'CFG'
[connection]
wifi.powersave = 2
CFG
sudo systemctl restart NetworkManager
```

Now your Pico can join `LampAP` with the PSK and talk to the Flask app at `http://192.168.50.1/`.

> Prefer to isolate? That AP is a self-contained network. If this Pi Zero also has Ethernet to your LAN and you *don’t* want clients to escape the AP, skip bridging and keep the default “shared” without a working uplink; that still provides DHCP to the Pico but no Internet.

---

# 5) Pico request targets (for clarity)

* Toggle: `http://192.168.50.1/gpio/toggle`
* On: `http://192.168.50.1/gpio/on`
* Off: `http://192.168.50.1/gpio/off`
* Status JSON: `http://192.168.50.1/lamp-status/`  → `{"lamp_pin_status": "ON"}` (or `"OFF"`)

*(If you want, I can drop in a tiny MicroPython snippet for the Pico that connects to SSID + does a `urequests.get()` to `/gpio/toggle`.)*

---

# 6) Security & reliability touches (recommended)

1. **Firewall (UFW)**: only allow HTTP from the AP subnet.

   ```bash
   sudo apt install -y ufw
   sudo ufw default deny incoming
   sudo ufw allow from 192.168.50.0/24 to any port 80 proto tcp
   sudo ufw enable
   sudo ufw status verbose
   ```

2. **Graceful hardware errors**: ensure `hardware_control.py` won’t crash Gunicorn if GPIO init fails. Return a 503 or a friendly message.

3. **Config via env** (future-proof): make the pin overridable.

   ```python
   import os
   lamp_control_pin = int(os.getenv("LAMP_PIN", 24))
   ```

   Then in the unit:

   ```ini
   Environment=LAMP_PIN=24
   ```

4. **Health endpoint**: add `/healthz` that returns `200 OK` quickly (no GPIO access). Nginx can use it for simple checks.

5. **Logging**: gunicorn `--access-logfile -` if you want per-request logs in `journalctl`.
   Example:

   ```ini
   ExecStart=... gunicorn --workers 1 --threads 2 --access-logfile - --bind unix:/run/gunicorn-lamp/socket wsgi:app
   ```

6. **Static “panel” page**: Consider a tiny HTML status page that polls `/lamp-status/` every 1–2s and has “On/Off/Toggle” buttons (handy from a phone).

7. **Pin persistence on reboot**: if you need a default state (e.g., default OFF), ensure `HardwareControl` sets it on init, and the relay module you use is “active-low/active-high” matched to your code.

8. **Backups**: keep `/srv/lamp` in `git`; back up `/etc/nginx/sites-available/lamp` and `/etc/systemd/system/gunicorn-lamp.service`.

---

# 7) What Nginx does (in one paragraph)

Nginx is a high-performance web server and reverse proxy. In this setup it receives HTTP from clients (your Pico or a phone), handles connection concurrency efficiently, and passes requests to Gunicorn over a local UNIX socket. It can also serve static files, add security headers, enforce request size/time limits, and (if you ever want) terminate TLS—letting your Python app stay simple and focused.

---

## Quick verification checklist

* `systemctl status gunicorn-lamp` → active (running)
* `curl http://127.0.0.1/lamp-status/` on the Pi → JSON
* `nmcli con show lamp-ap` → activated, IP `192.168.50.1`
* Phone or laptop can join **LampAP** and `curl http://192.168.50.1/gpio/toggle` works
* `journalctl -u gunicorn-lamp -f` shows requests arriving

If you’d like, I can also:

* Add a minimal `/healthz` route and a tiny static control panel page.
* Provide a ready-to-paste Pico MicroPython snippet for joining the AP and hitting the endpoints.
* Convert your app to read the pin from env + add a `requirements.txt`.
