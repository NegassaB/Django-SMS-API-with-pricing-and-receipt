"""
This module is used to send the necessary request to ethio-telecom server and
gets a response back. It uses the requests library.
"""
# don't be a dummy...use a try/except/else block
import requests


def sender(sms_data):
    """
    The actual method that accesses ethio-telecom's server and send the sms.
    It runs on a thread b/c it will recieve multiple requests.
    """
    ethio_telecom_url = "http://10.8.0.86:5000/api/sendsms/"
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.request(
        "POST",
        ethio_telecom_url,
        data=sms_data,
        headers=headers
    )
    if response.status_code == 201:
        return True
    else:
        return False


def retry(sms_data):
    """
    This method retry's to send the sms in 10 second's time if it has
    failed via the sender() method.
    """
    ethio_telecom_url = "http://10.8.0.86:5000/api/sendsms/"
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.request(
        "POST",
        ethio_telecom_url,
        data=sms_data,
        headers=headers
    )
    if response.status_code == 201:
        return True
    else:
        return False
