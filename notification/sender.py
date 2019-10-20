"""
This module is used to send the necessary request to ethio-telecom server and
gets a response back. It uses the requests library.
"""
# don't be a dummy...use a try/except/else block
import requests
from requests.adapters import HTTPAdapter
import time
from datetime import datetime

from rest_framework.response import Response
from rest_framework import status


def sender(sms_data):
    """
    The actual function that accesses the server and sends the sms.
    """
    sending_url = "http://127.0.0.1:5000/api/sendsms/"
    sending_headers = {"content-type": "application/x-www-form-urlencoded"}

    resp = requests.Response()
    try:
        resp = requests.post(
            sending_url,
            data=sms_data,
            headers=sending_headers,
            timeout=(3, 6),
        )
        with open('output.txt', 'a') as response_obejcts:
            response_obejcts.write(resp.content)
        resp.raise_for_status()
    except Exception as e:
        # TODO: find a better thing to do with the exception
        return False, resp
    else:
        return True, resp
