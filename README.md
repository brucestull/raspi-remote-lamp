# Remote GPIO Control with Flask (pin 17)

Flask app to control GPIO pin 17 from remote web browser.

## Commits

### [Commit bed677eb3e56576d0e2b8cdad42fda427d910dba](https://github.com/brucestull/raspi-zero-lamp-server/tree/bed677eb3e56576d0e2b8cdad42fda427d910dba)

- Raspberry Pi Zero connects to local WiFi
- Raspberry Pi Pico connects to local WiFi
- Functional endpoints
    - `/gpio/`
    - `/gpio/lamp-status/`
    - `/gpio/on`
    - `/gpio/off`

## Links

- [http://192.168.4.1:8000/gpio/](http://192.168.4.1:8000/gpio/)
- [http://192.168.4.1:8000/gpio/on](http://192.168.4.1:8000/gpio/on)
- [http://192.168.4.1:8000/gpio/off](http://192.168.4.1:8000/gpio/off)
- [http://192.168.4.1:8000/gpio/on?](http://192.168.4.1:8000/gpio/on?)
- [http://192.168.4.1:8000/gpio/off?](http://192.168.4.1:8000/gpio/off?)


## Links and URLS

- [http://192.168.1.91:8000/lamp-status/](http://192.168.1.91:8000/lamp-status/)
- [http://192.168.1.91:8000/gpio/](http://192.168.1.91:8000/gpio/)
- [http://192.168.1.91:8000/gpio/on](http://192.168.1.91:8000/gpio/on)
- [http://192.168.1.91:8000/gpio/off](http://192.168.1.91:8000/gpio/off)

- `curl http://192.168.1.91:8000/lamp-status/`
- `curl http://192.168.1.91:8000/gpio/`
- `curl http://192.168.1.91:8000/gpio/on`
- `curl http://192.168.1.91:8000/gpio/off`

## Setup

### Raspberry Pi - Running Raspberry Pi OS

1. `sudo apt-get update && sudo apt-get upgrade -y`
1. `sudo apt-get install git`
1. `sudo apt-get install pipenv`
1. `ssh-keygen -t ed25519 -C "name@email.app"`
1. `eval "$(ssh-agent -s)"`
1. `ssh-add ~/.ssh/id_ed25519`
1. `cat ~/.ssh/id_ed25519*`
1. [https://github.com/settings/keys](https://github.com/settings/keys)
1. `ssh -T git@github.com`
1. `git config --global user.email "name@email.app"`
1. `git config --global user.name "Name"`
1. `git clone <REPOSITORY_URL>`
1. `cd <REPOSITORY_DIRECTORY>`
1. `pipenv install`
