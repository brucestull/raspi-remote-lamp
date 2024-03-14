import requests


def send_request(url, path):
    """
    Send a request to the specified URL.

    :param url: The URL to send the request to.
    :type url: str
    :param path: The path to append to the URL.
    :type path: str
    """
    response = requests.get(f"http://{url}{path}")
    print(response.text)
    response.close()
