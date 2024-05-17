"""
This module is used to send the necessary request to ethio-telecom server and
gets a response back. It uses the requests library.
"""

import requests
import time
import json
from queue import Queue
import uuid


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
        time.sleep(2)
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


def safari_sender(data_to_send):
    sms_number_to, sms_content = data_to_send.get("number"), data_to_send.get(
        "msg_text"
    )
    PROD_PERSONAL_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiYTgyODc1NGRmYTg2N2M3ZjJmYjg3MTg5ZmU4MzAzNzY0YjZjZDMyYzExYWM4Nzk5OGFlY2Y2OTU4ODY0NDZhNjBmMWQ4MDQ5YjlkMDQyMTUiLCJpYXQiOjE3MDU2NzQ0ODksIm5iZiI6MTcwNTY3NDQ4OSwiZXhwIjo0ODYxMzQ4MDg5LCJzdWIiOiI0NSIsInNjb3BlcyI6W119.mk4fmhM6tCyYdNYVYv7BR-3yGdJXXIlc6rpuwvNFp69PvITvLdau8RtJus791wHg1BG6AkkuAkQyNTcL9SrFZMWWPW0pQb3qcuBeIbTcfAp8ICtYseVxjGJISOkzd4ZtIzxRZU33Umej64nr_mtIWtSv8-3BM6ZiHeG1m6pPK1rfmTtVcXn-pcESu8yqCJFoRLf7GIDMZCZeks6GyDbPcdy4IBrwB6BCaoILqMcyefMypwdisMBIiXQl7lpNUd2Oq8GKndQzRoNY_bwzgJ-JnV-vs9q1u9TY2GguGduZrlm1OAxCSeX2QB5GDkpf9XpXOgULWyo-0JmH63ELQpY3A6wYR-BmMqjPhLbSfAdLmkMJCumn87NT_BZA0zlag03XcZqqV-JdwKiOHAYsWKB5VtWFMEG6zQry8Pk1wexsSoqOi1tUqdSgJV40duhLzMts9b6VGqpvKuwaSCM4tV-okAMZVjLM19K--ZHHNK34QlaU8BRJx96Fi46-JCouC3d8rf-M5qQ1_D9U4b1HSLznJe8xEmjlbyE6X05vf_J99ubCiru-a298hZndSa6wZv6oRTJpwtmmI3MtIz_l4AZSDfz8_ggqZC4SFY3aCaBIwEi24VvRPqvj_fpuErKig0ERXxehTzjcOv6Q9PCl1QoGMgGjbzilEJRTMR0Y1YaVID0"
    PROD_HEADERS = f"Bearer {PROD_PERSONAL_ACCESS_TOKEN}"
    BULK_BASE = "https://bsms-business.safaricom.et/api/v1"
    payload = {
        "sender": "KEKROS",
        "message": f"{sms_content}",
        "phone": f"{sms_number_to[1:]}",
        "correlator": f"{uuid.uuid4()}",
        "endpoint": "https://api-et.sms.et/notification/safari-receipt/",
    }

    response = requests.Response()
    try:
        response = requests.post(
            #verify="/var/www/api-et.sms.et/notification/bsms-business-safaricom-et-chain.pem",
            #verify=False,
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
