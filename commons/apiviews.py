"""
This is the file responsible for generating the necessary views of the api.
"""

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404, get_list_or_404

from commons.models import SMSUser, SMSPrice, Type
from commons.serializers import SMSUserSerializer, SMSPriceSerializer, TypeSerializer


class SMSUserViewSet(viewsets.ModelViewSet):
    """
    This class is responsible for creating the viewset
    (As we decided to use viewset for the SMSUser model) for the SMSUser model.
    It sub-classes the ModelViewSet of the rest_framework.
    """
    queryset = SMSUser.objects.all()
    serializer_class = SMSUserSerializer


class TypeList(generics.ListCreateAPIView):
    """
    This class is responsible for generating, and returning, the view for all created objects of the Type model.
    It sub-classes the ListCreateAPIView class of the generics module.
    """

    queryset = Type.objects.all()
    if not queryset:
        Response(data={"{0} not found".format(queryset)}, status=404, content_type="application/json")
    serializer_class = TypeSerializer


class TypeDetail(generics.RetrieveAPIView):
    """
    This class is responsible for generating, and returning, the view of a single created object of the Type model.
    It sub-classes the RetrieveDestroyAPIView class of the generics module.
    If it finds the requested object it will return it, but if it doesn't it will return a 404.
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
