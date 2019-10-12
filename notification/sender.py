"""
This module is used to send the necessary request to ethio-telecom server and
gets a response back. It uses the requests library.
"""
# don't be a dummy...use a try/except/else block
import requests
from threading import Thread
import queue
import concurrent.futures

from rest_framework.response import Response
from rest_framework import status


def sender_utility(sms_data):
    """
    inputs sms data to sender_utility(), puts sms data into a queue,
    copies 14 items from sms_queue to pipeline, sends as input parameter to sender()
    """
    sms_queue = queue.Queue()
    sms_queue.put(sms_data)

    pipeline = queue.Queue(maxsize=13)
    # TODO: do this in a thread and once the pipeline is full, aka,
    # 14 sms's call thread sleep until all sms's are sent
    while pipeline.qsize() <= 14:
        pipeline.put(sms_queue.get())

    if not send_sms(pipeline):
        return False
    else:
        return True


def send_sms(pipeline):
    # TODO: documentation for this function
    while not pipeline.qsize == 0:
        sender(pipeline.get())
    # if not pipeline.qsize == 0:
    if not pipeline.empty():
        pipeline.join()


def sender(sms_data):
    """
    The actual method that accesses ethio-telecom's server and send the sms.
    """
    ethio_telecom_url = "http://10.8.0.86:5000/api/sendsms/"
    headers = {"content-type": "application/x-www-form-urlencoded"}

    try:
        response = requests.request(
            "POST",
            ethio_telecom_url,
            data=sms_data,
            headers=headers
        )
    except Exception as e:
        # TODO: find a better thing to do with the exception
        return Response(
            data={
                "error": str(e)
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
            headers=str(e.args(1))
        )
    else:
        return Response(
            data={
                "message": "sms text sent successfully!"
            },
            status=status.HTTP_200_OK
        )
