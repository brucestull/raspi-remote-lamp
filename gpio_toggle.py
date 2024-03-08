from utils import send_request
from time import sleep

URL = "192.168.1.181"
LED_ON_PATH = "/gpio/on"
LED_OFF_PATH = "/gpio/off"


def main():
    sleep(2)
    print("Sending request to turn LED on...")
    send_request(URL, LED_ON_PATH)
    sleep(2)
    print("Sending request to turn LED off...")
    send_request(URL, LED_OFF_PATH)
    sleep(2)
    print("Sending request to turn LED on...")
    send_request(URL, LED_ON_PATH)
    sleep(2)
    print("Sending request to turn LED off...")
    send_request(URL, LED_OFF_PATH)


if __name__ == "__main__":
    main()
