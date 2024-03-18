from time import sleep

from utils import send_request

HOST = "192.168.1.91"
PORT = 8000
ROOT_URL = f"{HOST}:{PORT}"
LED_ON_PATH = "/gpio/on"
LED_OFF_PATH = "/gpio/off"


def main():
    sleep(3)
    print("Sending request to turn LED on...")
    send_request(ROOT_URL, LED_ON_PATH)
    sleep(3)
    print("Sending request to turn LED off...")
    send_request(ROOT_URL, LED_OFF_PATH)
    sleep(3)
    print("Sending request to turn LED on...")
    send_request(ROOT_URL, LED_ON_PATH)
    sleep(3)
    print("Sending request to turn LED off...")
    send_request(ROOT_URL, LED_OFF_PATH)


if __name__ == "__main__":
    main()
