"""
This file is responsible for generating the api views for the notification app.
"""

from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate

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


class SMSendView(APIView):
    """
    This class is responsible for sending an sms. It send a valid, necessary bundled up data to the sender() method from
    the notification.sender module. Once it recieves a boolean value from that module it updates the instance and saves it to the db.
    """

    serializer_class = SMSMessagesSerializer

    def post(self, request):
        """
        This method is used to create an instance of the SMSMessages indirectly by using the SMSMessagesSerializer.
        If that is valid it will be passed to the sender() method from the notification.sender module. Once that returns
        a True value the serializer will be saved, aka the object will be saved to the database with a delivery_status value
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
                "phone_number": sms_messages_serializer.data.get(
                    "sms_number_to"
                ),
                "content": sms_messages_serializer.data.get(
                    "sms_content"
                )
                }
            if sender(data_to_send):
                # The below is left as reminder of how you did it first
                # sms_messages_serializer.update(data={"delivery_status": True}, partial=True)
                sms_messages_serializer.update(instance, validated_data={"delivery_status": True})
                sms_messages_serializer.save()
                return Response(
                    data={
                        "success": "You have successfully sent the sms"
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                if not retry(data_to_send):
                    sms_messages_serializer.update(instance, validated_data={"delivery_status": True})
                    sms_messages_serializer.save()
                    return Response(
                        data={
                            "success": "You have successfully sent the sms"
                        },
                        status=status.HTTP_201_CREATED
                    )
                    if not retry(data_to_send):
                        sms_messages_serializer.update(instance, validated_data={"delivery_status": True})
                        sms_messages_serializer.save()
                        return Response(
                            data={
                                "success": "You have successfully sent the sms"
                            },
                            status=status.HTTP_201_CREATED
                        )
                else:
                    sms_messages_serializer.update(instance, validated_data={"delivery_status": True})
                    sms_messages_serializer.save()
                    return Response(
                        data={
                            "error": "Your message has not been sent, please try again."
                        },
                        status=status.HTTP_504_GATEWAY_TIMEOUT
                    )
