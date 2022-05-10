import json
import requests
import logging
import time
from threading import Thread
from queue import Queue

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import renderer_classes

from commons.serializers import SMSMessagesSerializer


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class PhoneNumber():
    def __init__(self, phonenumber, content):
        self.phonenumber = phonenumber
        self.content = content

    def __repr__(self):
        return str({
            'type_of_obj': type(self),
            'phonenumber': self.phonenumber,
            'content': self.content,
        })


# queue_to_send: "Queue[PhoneNumber]" = Queue()
queue_to_send = Queue()


class BulkSender(generics.CreateAPIView):

    serializer_class = SMSMessagesSerializer

    @renderer_classes(JSONRenderer)
    def put(self, request):
        if not request.auth:
            return Response(
                data={"error": "unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json"
            )
        t = Thread(target=self.send_bulk, args=(request,))
        t.start()
        return Response(
            data={"success": "Request accepted, will be processed..."},
            status=status.HTTP_202_ACCEPTED,
            content_type="application/json"
        )

    def send_bulk(self, request):
        bulk_details = request.data
        auth_token = str(request.auth)
        phone_nums = bulk_details.get("phone_nums")
        bulk_content = bulk_details.get("bulk_content")
        for num in phone_nums:
            queue_to_send.put(PhoneNumber(num, bulk_content))

        while queue_to_send.empty() is False:
            num_2_send = queue_to_send.get()
            time.sleep(2)
            return self.sender(num_2_send.phonenumber, num_2_send.content, auth_token)
        else:
            logger.info("COMPLETED SENDING SMS")

    def sender(self, number, content, auth_token):
        url = "http://127.0.0.1:8055/notification/sendsms/"
        payload = json.dumps({"sms_number_to": f"{number}", "sms_content": f"{content}"})
        headers = {
            'content-type': "application/json",
            'authorization': f"token {auth_token}"
        }
        try:
            response = requests.post(
                url,
                data=payload,
                headers=headers
            )
        except Exception as e:
            logger.error("exception in bulk_sender(), {}".format(e), exc_info=True)
            print("something went wrong in bulk_sender(), check the log")
            return Response(
                    data={"error": f"sms sent to {number}"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                    content_type="application/json"
                )
        else:
            logger.info(f"from bulk_sender(), {response.text} -- {response.status_code}")
            return Response(
                    data={"success": f"sms sent to {number}"},
                    status=status.HTTP_202_ACCEPTED,
                    content_type="application/json"
                )
