"""
This is the file responsible for generating the necessary views of the api.
"""

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

from commons.models import SMSUser, SMSPrice, Type
from commons.serializers import SMSUserSerializer, SmSPriceSerializer, TypeSerializer


class SMSUserViewSet(viewsets.ModelViewSet):
    """
    This class is responsible for creating the viewset
    (As we decided to use viewset for the SMSUser model) for the SMSUser model.
    It sub-classes the ModelViewSet of the rest_framework.
    """
    queryset = SMSUser.objects.all()
    serializer_class = SMSUserSerializer


class TypeList(APIView):
    """ This class is responsible for generating the view for all created objects of the Type model.
    It sub-classes the APIView class of the rest_framework. """
    def get(self, request):
        """
        This method is responsible for orgainizing and returning the view.
        If the objects exist and it finds them it will send a Response object containing that data, but if it doesn't it will
        send a Response object built with a formatted data containing the message to be displayed , status code 200,
         and json content-type stating that the model doesn't have any objects.
        """
        # types = Type.objects.all()[:10]
        types = get_list_or_404(Type)
        data = TypeSerializer(types, many=True).data
        return Response(data)


class TypeDetail(APIView):
    """
    This class is responsible for generating the view of a single created object of the Type model.
    It sub-classes the APIView class of the rest_framework.
    """
    def get(self, request, key):
        """
        This method is responsible for actually retrieving the stated object, by the pk, from the Type model.
        If the requested object exists and the method finds, it will send a Response object containing that data,
        but if it doesn't the get_object_or_404() method will send a response showing a 404 object not found.
        pk stands for the primary key/id found in the table.
        """
        type = get_object_or_404(Type, pk=key)
        data = TypeSerializer(type).data
        return Response(data)
