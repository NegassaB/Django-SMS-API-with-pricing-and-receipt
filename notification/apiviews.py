"""
This file is responsible for generating the api views for the notification app.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.pagination import PageNumberPagination


import datetime
import time

from commons.models import SMSMessages
from commons.serializers import SMSMessagesSerializer
from notification.serializers import PhoneNumberSerializer
from notification.sender import place_in_queue, safari_sender


class SMSView(APIView, PageNumberPagination):
    """
    This class is responsible for all the method operations of an sms. It provides implementations for the GET, POST, and OPTIONS methods.
    Each method provides it's own description.
    """

    serializer_class = SMSMessagesSerializer

    def get(self, request):
        """
        This method is used to GET all created instance of the SMSMessages class that are saved in the db and if it's not None,
        it will return a paginated Response object constructed using the PageNumberPagination class and it's methods.
        """
        queryset = SMSMessages.objects.filter(sending_user=request.user).order_by("-id")
        while queryset:
            sms_serializer = SMSMessagesSerializer(
                self.paginate_queryset(queryset, request),
                many=True,
                context={"request": request},
            )
            return self.get_paginated_response(sms_serializer.data)
        else:
            return Response(
                data={"error": "no sms has been sent"},
                status=status.HTTP_404_NOT_FOUND,
                content_type="application/json",
            )

    @renderer_classes(JSONRenderer)
    def post(self, request):
        """
        This method is used to create an instance of the SMSMessages indirectly by using the SMSMessagesSerializer.
        If that is valid it will be passed to the sender() method from the notification.sender module. The serializer
        will be saved, aka the object will be saved to the database, and then sender() is called. Once that returns
        a True value the instance will be called, aka the object will be updated with a delivery_status value of True
        and saved to the database.
        """
        resp = Response()
        if not request.auth.user_id:
            return resp(
                data={"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json",
            )
        serialized_phone = PhoneNumberSerializer(data=request.data)
        if not serialized_phone.is_valid(raise_exception=True):
            resp = Response(
                data={"error": f"{serialized_phone.args}"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content_type="application/json",
            )
            print(
                f"{datetime.datetime.now()} -- {resp.status_code} -- {serialized_phone.args}"
            )
            return resp
        if (
            not request.data.get("sms_content")
            or len(request.data.get("sms_content")) > 160
        ):
            resp = Response(
                data={
                    "error": "sms_content must not be null or more than 160 characters."
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content_type="application/json",
            )
            print(
                f"{datetime.datetime.now()} -- {resp.status_code} -- {resp.status_text}"
            )
            return resp
        else:
            print(f"{datetime.datetime.now()} -- {request.data}")
            sms_number_to = serialized_phone.validated_data.get("sms_number_to")
            if sms_number_to.startswith("+2517"):
                data_to_send = {
                    "number": sms_number_to,
                    "msg_text": request.data.get("sms_content"),
                }
                status_flag, status_response = safari_sender(data_to_send)
            else:
                data_to_send = {
                    "number": sms_number_to,
                    "msg_text": request.data.get("sms_content"),
                }
                try:
                    SMSView.save_2_db(data_to_send, request.auth.user_id, False)
                except Exception as e:
                    print(f"exception on saving {e}, {data_to_send}")
                    resp = Response(
                        data={"error": f"{e}"},
                        status=status.HTTP_400_BAD_REQUEST,
                        content_type="application/json",
                    )
                    return resp
                time.sleep(1)
                status_flag, status_response = place_in_queue(data_to_send)

            if not status_flag:
                resp = Response(
                    data={"error": f"sms not sent {status_response.reason}"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                    content_type="application/json",
                )
                print(
                    f"{datetime.datetime.now()} -- {resp.status_code} -- {resp.status_text} -- {data_to_send['number']}"
                )
                return resp
            else:
                resp = Response(
                    data={"status": "success"},
                    status=status.HTTP_201_CREATED,
                    content_type="application/json",
                )
                SMSView.save_2_db(data_to_send, request.auth.user_id, True)
                print(
                    f"{datetime.datetime.now()} -- {resp.status_code} -- {resp.status_text} -- {data_to_send['number']}"
                )
                return resp

    @classmethod
    def save_2_db(self, data_2_send, user_id, update_sms=False):
        sms_messages_serializer = SMSMessagesSerializer(
            data={
                "sms_number_to": data_2_send.get("number"),
                "sms_content": data_2_send.get("msg_text"),
                "sending_user": user_id,
                "delivery_status": update_sms,
            }
        )
        if sms_messages_serializer.is_valid():
            sms_messages_serializer.save()
        else:
            print(str(sms_messages_serializer.errors))
            raise Exception(str(sms_messages_serializer.errors))


class SMSCountView(APIView):
    serializer_class = SMSMessagesSerializer

    def get(self, request):
        total, delivered, failed = self.count_queryset(request)
        return Response(
            data={"total": total, "delivered": delivered, "failed": failed},
            status=status.HTTP_200_OK,
            content_type="application/json",
        )

    def count_queryset(self, request):
        val = datetime.datetime.now()
        queryset = SMSMessages.objects.filter(
            sending_user=request.user,
            sent_date__year=val.year,
            sent_date__month=val.month,
        )
        if queryset.exists():
            delivered_queryset = queryset.filter(delivery_status=True)
            failed_queryset = queryset.filter(delivery_status=False)
            total = queryset.count()
            delivered = delivered_queryset.count()
            failed = failed_queryset.count()
            return total, delivered, failed
        else:
            return 0, 0, 0


class SafariReceipt(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        return Response(status=status.HTTP_200_OK)
