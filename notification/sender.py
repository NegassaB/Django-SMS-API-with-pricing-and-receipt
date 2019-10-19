"""
This module is used to send the necessary request to ethio-telecom server and
gets a response back. It uses the requests library.
"""
# don't be a dummy...use a try/except/else block
import requests
import queue
import time
from datetime import datetime

from rest_framework.response import Response
from rest_framework import status


def sender_utility(sms_data):
    """
    inputs sms data to sender_utility(), puts sms data into a queue,
    copies 14 items from sms_queue to pipeline, sends as input parameter to sender()
    """
    time.sleep(2)
    sms_queue = queue.Queue()
    sms_queue.put(sms_data)

    pipeline = queue.Queue(maxsize=13)
    while pipeline.qsize() <= 14 and not sms_queue.empty():
        pipeline.put(sms_queue.get())

    if not send_sms(pipeline):
        return False
    else:
        return True


def send_sms(pipeline):
    """
    This function is used to to implement the sender() function on each
    individual text. It uses the pipeline transfered from sender_utility()
    and calls the get() method from queue for the sender() function.
    """
    while not pipeline.qsize == 0:
        sender(pipeline.get())
    # if not pipeline.qsize == 0:thread
    if not pipeline.empty():
        pipeline.join()

    return True


def sender(sms_data):
    """
    The actual function that accesses the server and sends the sms.
    """
    sending_url = "http://127.0.0.1:5000/api/sendsms/"
    headers = {"content-type": "application/x-www-form-urlencoded"}

    """
    Used for moitoring that the try block doesn't run forever but rather for 5 seconds.
    """
    start_time = datetime.now()
    start_second = start_time.second
    end_second = start_second + 5

    while start_second != end_second:
        start_second = start_second + 1
        # you might have to run either the counter or the try block in another
        # thread and keep track of that.
        try:
            response = requests.request(
                "POST",
                sending_url,
                data=sms_data,
                headers=headers
            )
            if response == None:
                return Response(data=response.data, status=response.status)
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
    else:
        return Response(
            data={
                "error": "unable to send sms!"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
