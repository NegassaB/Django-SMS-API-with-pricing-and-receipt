"""
This module is used to send the necessary request to ethio-telecom server and
gets a response back. It uses the requests library.
"""
import requests
import time
import json

from rest_framework.response import Response
from rest_framework import status

base_url_sdp = "http://10.8.0.86:5000/"

def sender(sms_data):
    """
    The actual function that accesses the server and sends the sms.
    """
    sending_url = base_url_sdp + "api/sendsms/"
    sending_headers = {"content-type": "application/json"}

    response = requests.Response()
    try:
        response = requests.post(
            sending_url,
            data=sms_data,
            headers=sending_headers,
            timeout=(3, 6)
        )
        response.raise_for_status()
        # TODO: log all responses from sms_server here and send your own responses to user
    except Exception as e:
        # TODO: find a better thing to do with the exception
        # perhaps a log file, like the below one
        print(response)
        return False, response
    else:
        print(response)
        return True, response
