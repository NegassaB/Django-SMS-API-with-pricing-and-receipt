"""
This file is responsible for generating the api views for the notification app.
"""

from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate

import threading
import datetime

from commons.models import SMSMessages
from commons.serializers import SMSMessagesSerializer
from notification.sender import sender


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
                    queryset.values()
                    },
                status=status.HTTP_200_OK,
                content_type="application/json"
            )
        else:
            return Response(
                data={
                    "no sms has been sent"
                },
                status=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )

    def post(self, request):
        """
        This method is used to create an instance of the SMSMessages indirectly by using the SMSMessagesSerializer.
        If that is valid it will be passed to the sender_utility() method from the notification.sender module. The serializer
        will be saved, , aka the object will be saved to the database and then the sender_utility() called.Once that returns
        a True value the instance will be called, aka the object will be saved to the database with a delivery_status value
        of True.
        """
        sms_messages_serializer = SMSMessagesSerializer(
            data={
                "sms_number_to": request.data.get("sms_number_to"),
                "sms_content": request.data.get("sms_content"),
                "sending_user": request.data.get("sending_user")
            }
        )
        permission_classes = (permissions.IsAuthenticated)

        if sms_messages_serializer.is_valid():
            data_to_send = {
                "phone_number": sms_messages_serializer.validated_data[
                    "sms_number_to"
                ],
                "content": sms_messages_serializer.validated_data[
                    "sms_content"
                ]
            }
            sms_messages_serializer.save()

        # TODO this is used to test so find a better name
        run_again = True
        while run_again:
            # the following are the return values of the
            # sender() function from the notification.sender module
            # TODO find better names
            x, y = sender(data_to_send)
            if not x:
                return Response(
                    data={
                        "error": f"{y.text}"
                    },
                    status=y.status_code,
                    content_type="application/json"
                )
            else:
                sms_messages_serializer.update(
                    data={
                        "delivery_status": True
                    },
                    partial=True
                )
                run_again = False
                return Response(
                    data={
                        "success": f"{y.json()}"
                    },
                    headers=y.headers,
                    status=y.status_code,
                    content_type="application/json"
                )
        else:
            run_again = False
            return Response(
                data={
                    "error": "unable to send sms"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json"
            )
