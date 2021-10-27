"""
This file is responsible for generating the api views for the notification app.
"""

from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate

import threading
import datetime
import json
import time

from commons.models import SMSMessages
from commons.serializers import SMSMessagesSerializer
from notification.sender import place_in_queue, telegram_sender


class SMSMessagesView(generics.ListCreateAPIView):

    """
    This class is responsible for generating, and returning, the view for all created objects of the SMSMessages model.
    It sub-classes the ListCreateAPIView class of the generics module.
    """
    queryset = SMSMessages.objects.all()
    if not queryset:
        Response(data={"{0} not found".format(queryset)}, status=404, content_type="application/json")

    serializer_class = SMSMessagesSerializer


class SMSView(APIView):
    """
    This class is responsible for all the method operations of an sms. It provides implementations for the GET, POST, and OPTIONS methods.
    Each method provides it's own description.
    """

    serializer_class = SMSMessagesSerializer

    def get(self, request):
        """
        This method is used to GET all created instance of the SMSMessages class that are saved in the db.
        """
        queryset = SMSMessages.objects.filter(sending_user=request.user)
        while queryset:
            return Response(
                data={
                    'result_objects': queryset.values()
                    },
                status=status.HTTP_200_OK,
                content_type="application/json"
            )
        else:
            return Response(
                data={
                    'result_objects': "no sms has been sent"
                },
                status=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )

    @renderer_classes(JSONRenderer)
    def post(self, request):
        """
        This method is used to create an instance of the SMSMessages indirectly by using the SMSMessagesSerializer.
        If that is valid it will be passed to the sender() method from the notification.sender module. The serializer
        will be saved, aka the object will be saved to the database, and then the sender() is called. It will run three
        times before it gives up and fails. Once that returns a True value the instance will be called, aka the object
        will be saved to the database, with a delivery_status value of True.
        """
        resp = Response()
        sms_messages_serializer = SMSMessagesSerializer(
            data={
                "sms_number_to": request.data.get("sms_number_to"),
                "sms_content": request.data.get("sms_content"),
                "sending_user": request.auth.user_id,
            }
        )
        permission_classes = (permissions.IsAuthenticated)

        if sms_messages_serializer.is_valid():
            data_to_send = {
                "number": sms_messages_serializer.validated_data[
                    "sms_number_to"
                ],
                "msg_text": sms_messages_serializer.validated_data[
                    "sms_content"
                ]
            }
            # used for the instance, find a better name
            sms_object = sms_messages_serializer.save()
        else:
            print(str(sms_messages_serializer.errors))
            data_to_send = None
            resp = Response(
                data={
                    "error": f"{sms_messages_serializer.errors}"
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content_type="application/json"
            )
            print(f"{datetime.datetime.now()} -- {resp.status_code} -- {resp.status_text}")
            return resp

        # TODO refactor this into it's own function

        time.sleep(2)
        status_flag, status_response = place_in_queue(data_to_send)
        telegram_sender(data_to_send)

        if not status_flag:
            resp = Response(
                data={
                    "error": "sms not sent"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
                content_type="application/json"
            )
            print(f"{datetime.datetime.now()} -- {resp.status_code} -- {resp.status_text}")
            return resp
        else:
            # the update method defined in the SMSMessagesSerializer class
            # needs an instance to run with, so that's what has been changed.
            # The data attribute has been removed.
            sms_messages_serializer.update(
                sms_object,
                {
                    "delivery_status": True
                }
            )
            resp = Response(
                data={
                    "status": "success"
                },
                status=status.HTTP_201_CREATED,
                content_type="application/json"
            )
            print(f"{datetime.datetime.now()} -- {resp.status_code} -- {resp.status_text}")
            return resp
