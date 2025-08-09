"""
This module is used to send the necessary request to ethio-telecom server and
gets a response back. It uses the requests library.
"""

import requests
import time
import json
from queue import Queue
import uuid


base_url_sdp = "SENDING_URL"

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
    telegram_sms_data["number"] = sms_data.get("number")
    telegram_sms_data["msg_txt"] = sms_data.get("msg_text")
    try:
        res = requests.post(
            "http://gargarsa.sms.et/telegram_sender/",
            data=json.dumps(telegram_sms_data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        res.raise_for_status()
    except (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.ProxyError,
    ) as e:
        print(f"from telegram_sender -- {e}")
    else:
        print(f"telegram_sender -- {res} -- {res.reason}")


def sender(sms_data):
    """
    The actual function that accesses the server and sends the sms.
    """
    sending_url = base_url_sdp + "api/sendsms/"
    sending_headers = {"content-type": "application/x-www-form-urlencoded"}

    response = requests.Response()
    try:
        response = requests.post(
            sending_url, data=sms_data, headers=sending_headers, timeout=(4, 7)
        )
        response.raise_for_status()
    except Exception as e:
        print(str(e))
        print(
            f"RESPONSE {response.status_code} -- {response.headers} -- {response.reason}"
        )
        return False, response
    else:
        return True, response


def another_sender(data_to_send):
    sms_number_to, sms_content = (
        data_to_send.get("number"),
        data_to_send.get("msg_text"),
    )
    PROD_PERSONAL_ACCESS_TOKEN = ""
    PROD_HEADERS = f"Bearer {PROD_PERSONAL_ACCESS_TOKEN}"
    BULK_BASE = "BULK_URL"
    payload = {
        "sender": "SENDING_ID",
        "message": f"{sms_content}",
        "phone": f"{sms_number_to[1:]}",
        "correlator": f"{uuid.uuid4()}",
        "endpoint": "WEBHOOK_URL",
    }

    response = requests.Response()
    try:
        response = requests.post(
            url=f"{BULK_BASE}/send-sms/",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Connection": "Keep-Alive",
                "Authorization": PROD_HEADERS,
            },
            json=payload,
        )
        response.raise_for_status()
    except Exception as e:
        print(str(e))
        print(
            f"RESPONSE {response.status_code} -- {response.headers} -- {response.reason}"
        )
        return False, response
    else:
        return True, response
