"""
This module is used to send the necessary request to ethio-telecom server and
gets a response back. It uses the requests library.
"""
import requests
import time
import json
from queue import Queue

from rest_framework.response import Response
from rest_framework import status


base_url_sdp = "http://10.10.0.14:5000/"

sms_queue = Queue()


def place_in_queue(sms_data):
    """
    place_in_queue: used to place the sms that will be sent into a queue and
                    then it calls sender() using the data.

    Args:
        sms_data (Dict): a dict object recevied from apiviews.SMSView.post
    """
    sms_queue.put(sms_data)
    time.sleep(1)
    return sender(sms_queue.get())


def telegram_sender(sms_data):
    telegram_sms_data = {}
    telegram_sms_data['number'] = sms_data.get('number')
    telegram_sms_data['msg_txt'] = sms_data.get('msg_text')
    try:
        res = requests.post(
            "http://gargarsa.sms.et/telegram_sender/",
            data=json.dumps(telegram_sms_data),
            headers={"accept": "application/json", "Content-Type": "application/json"}
        )
        res.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.ProxyError) as e:
        print(f"from telegram_sender -- {e}")


def sender(sms_data):
    """
    The actual function that accesses the server and sends the sms.
    """
    sending_url = base_url_sdp + "api/sendsms/"
    sending_headers = {"content-type": "application/x-www-form-urlencoded"}

    response = requests.Response()
    try:
        time.sleep(2)
        response = requests.post(
            sending_url,
            data=sms_data,
            headers=sending_headers,
            timeout=(3, 6)
        )
        response.raise_for_status()
    except Exception as e:
        print(str(e))
        return False, response
    else:
        return True, response
