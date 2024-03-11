# Connect Raspberry Pi Dongle

[Connect Raspberry Pi Dongle - ChatGPT](https://chat.openai.com/share/438c8112-fe69-44e5-ab61-f0de14e0aabc)

[Connect Raspberry Pi Dongle - Unshared](https://chat.openai.com/c/e7243416-60c3-4dc1-b386-9c2e31fc2619)

## Request

I have a Raspberry Pi Zero set up as an access point. It's function it so provide access point services and serve up a hosted flask app.

I now want to add a USB WiFi dongle and use it to connect the Raspberry Pi Zero to my local network so it can access the internet.

I already have the WiFi dongle.

How do I connect this Raspberry Pi Zero (which is an access point) to my local WiFi network?

### Answer

To connect your Raspberry Pi Zero, which is already set up as an access point, to your local WiFi network using a USB WiFi dongle, you'll need to follow a series of steps. These steps will help you configure the Raspberry Pi Zero to connect to your local network for internet access while maintaining its function as an access point. Here's a general outline of the process:

### 1. Install the USB WiFi Dongle

First, ensure that your USB WiFi dongle is compatible with the Raspberry Pi Zero and that it is recognized by the system. Plug in the dongle and check if it's detected with the `lsusb` command.

### 2. Configure the Network Interface

You'll need to edit the network interface configuration file to set up the dongle to connect to your local WiFi network.

- Open the `/etc/network/interfaces` or the `/etc/dhcpcd.conf` file (depending on your system's configuration) in a text editor. For modern Raspberry Pi OS versions, `dhcpcd` is used, so you'd edit `/etc/dhcpcd.conf`.
- Add or modify the configuration for the WiFi dongle interface (usually `wlan1` if the built-in WiFi is `wlan0`). For `dhcpcd.conf`, you might add something like:

  ```
  interface wlan1
  static ip_address=192.168.x.x/24
  static routers=192.168.x.x
  static domain_name_servers=192.168.x.x 8.8.8.8
  ```

  Or for WiFi connection:

  ```
  profile static_wlan1
  static ip_address=192.168.x.x/24
  static routers=192.168.x.x
  static domain_name_servers=192.168.x.x 8.8.8.8

  interface wlan1
  ssid "YourSSID"
  psk "YourPassword"
  ```

Replace `"YourSSID"` and `"YourPassword"` with your WiFi network's SSID and password, respectively. Adjust the IP configuration (`192.168.x.x`) according to your network setup.

### 3. Set Up WiFi Connection

For the dongle to connect to your WiFi, ensure you've set up the correct SSID and password. This might involve editing the `wpa_supplicant.conf` file if your setup uses `wpa_supplicant` for managing WiFi connections:

- Edit or create the file `/etc/wpa_supplicant/wpa_supplicant-wlan1.conf` (for the dongle, hence `wlan1`), adding:

  ```
  ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
  update_config=1
  country=GB

  network={
      ssid="YourSSID"
      psk="YourPassword"
  }
  ```

  Replace `GB` with your country code, `"YourSSID"` with your WiFi network's name, and `"YourPassword"` with your WiFi password.

### 4. Enable Routing and IP Masquerading

If you haven't already, you'll need to enable IP forwarding and set up IP masquerading to allow devices connected to the access point to access the internet through the Raspberry Pi's other network interface (the dongle).

- Edit `/etc/sysctl.conf` and uncomment or add:

  ```
  net.ipv4.ip_forward=1
  ```

- Add IP masquerading rules via `iptables`. For example:

  ```
  sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
  sudo iptables -A FORWARD -i wlan1 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
  sudo iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT
  ```

  These commands configure NAT to forward traffic from the AP interface (`wlan0`) to the dongle interface (`wlan1`) and vice versa. Replace `wlan0` and `wlan1` with the correct interface names for your setup.

- Save the `iptables` rules to ensure they persist after reboot. The method to do this varies by distribution but might involve using `iptables-save` and `iptables-restore` with a file, such as `/etc/iptables.ipv4.nat`.

### 5. Restart Services

After making these changes, restart the affected services or simply reboot your Raspberry Pi:

```bash
sudo systemctl daemon-reload
sudo systemctl restart dhcpcd
sudo reboot
```

This process should enable your Raspberry Pi Zero to connect to the internet via the USB WiFi dongle while still functioning as an access point for other devices. Remember, the exact steps might vary slightly based on your specific setup and the versions of the operating system and software you're using.
