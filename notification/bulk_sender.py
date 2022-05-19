import datetime
import logging
import time
from threading import Thread
from queue import Queue

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import renderer_classes

from commons.serializers import SMSMessagesSerializer
from notification.sender import place_in_queue, telegram_sender


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class PhoneNumber():
    # queue_to_send: "Queue[PhoneNumber]" = Queue()
    queue_to_send = Queue()

    def __init__(self, phonenumber, content):
        self.phonenumber = phonenumber
        self.content = content

    @classmethod
    def insert_in_queue(self, numbers, bulk_sms_content):
        for num in numbers:
            PhoneNumber.queue_to_send.put(PhoneNumber(num, bulk_sms_content))

    def __repr__(self):
        return str(
            {
                'type_of_obj': type(self),
                'phonenumber': self.phonenumber,
                'content': self.content,
            }
        )


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
            data={"success": "Request accepted, it will be processed and sent..."},
            status=status.HTTP_202_ACCEPTED,
            content_type="application/json"
        )

    def send_bulk(self, request):
        phone_nums = request.data.get("phone_nums")
        bulk_content = request.data.get("bulk_content")
        PhoneNumber.insert_in_queue(phone_nums, bulk_content)

        while PhoneNumber.queue_to_send.empty() is False:
            num_2_send = PhoneNumber.queue_to_send.get()
            time.sleep(2)
            data_to_send = {
                "number": num_2_send.phonenumber,
                "msg_text": num_2_send.content
            }

            status_flag, status_response = place_in_queue(data_to_send)
            telegram_sender(data_to_send)

            resp = self.generate_response(status_response)
            BulkSender.save_2_db(data_to_send, request.auth.user_id, False)
            print(f"{datetime.datetime.now()} -- {resp.status_code} -- {resp.status_text} -- {data_to_send['number']}")
        else:
            logger.info("COMPLETED SENDING SMS")

    def generate_response(self, status_response):
        if status_response != 200:
            return Response(
                data={"error": "sms not sent"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
                content_type="application/json"
            )
        else:
            return Response(
                data={"status": "success"},
                status=status.HTTP_201_CREATED,
                content_type="application/json"
            )

    @classmethod
    def save_2_db(self, data_2_send, user_id, update_sms=False):
        sms_messages_serializer = SMSMessagesSerializer(
            data={
                "sms_number_to": data_2_send.get("number"),
                "sms_content": data_2_send.get("msg_text"),
                "sending_user": user_id,
                "delivery_status": update_sms
            }
        )
        if sms_messages_serializer.is_valid():
            sms_messages_serializer.save()
        else:
            print(str(sms_messages_serializer.errors))
