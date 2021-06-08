"""
This module is responsible for retry the failed sms's by checking their delivery_status
and thier sent_date. If the sent_date is more than an hour and the delivery_status is
False, this module will retry to send the sms all over again.
It uses the notification.sender module to send the sms and runs indefinately.
"""
from commons.models import SMSMessages
from django.db import models
from datetime import timedelta
from django.utils import timezone
import json
from requests import Response
from notification.sender import *

"""
It retries all the sms that have failed to be sent by filter all the created sms according
to their delivery_status (which would be False if it fails) and how long has it been since
it was created (anything younger than an hour is rejected)
"""

def send_utility(sms_data_to_send):
    max_retry = 0
    resp = Response()
    while max_retry < 3:
        max_retry += 1
        status_flag, status_response = sender(sms_data_to_send)
        if not status_flag:
            resp = Response(
                data={
                    "error": f"{status_response.text}"
                },
                status=status_response.status_code,
                content_type="application/json"
            )
        else:
            sms_messages_serializer.update(
                data={
                    "delivery_status": True
                },
                partial=True
            )
            resp = Response(
                data={
                    "success": f"{status_response.json()}"
                },
                headers=status_response.headers,
                status=status_response.status_code,
                content_type="application/json"
            )
            return resp
    else:
        resp = Response(
            data={
                "error": "unable to send sms"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type="application/json"
        )
        return resp

time_parameter = timezone.now() - timedelta(hours=1)
queryset = SMSMessages.objects.filter(sent_date__lt=time_parameter, delivery_status=False)

for sms_data in queryset:
    data_to_send = {
        "number": sms_data.sms_number_to,
        "msg_text": sms_data.sms_content
    }

    send_utility(json.dumps(data_to_send))


# TODO refactor this into it's own function

