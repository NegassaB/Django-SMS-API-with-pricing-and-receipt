"""
This is the file responsible for generating the necessary views of the commons app.
"""
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate

from commons.models import SMSUser, SMSPrice, Type, SMSMessages
from commons.serializers import SMSUserSerializer, SMSPriceSerializer, TypeSerializer, SMSMessagesSerializer


class SMSUserViewSet(viewsets.ModelViewSet):
    """
    This class is responsible for creating the viewset
    (As we decided to use viewset for the SMSUser model) for the SMSUser model.
    It sub-classes the ModelViewSet of the rest_framework.
    """
    authentication_classes = ()
    permission_classes = ()
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


class SMSPriceList(generics.ListCreateAPIView):
    """
    This class is responsible for generating, and returning, the view for all created objects of the SMSPrice model.
    It sub-classes the ListCreateAPIView class of the generics module.
    """

    queryset = SMSPrice.objects.all()
    if not queryset:
        Response(data={"{0} not found".format(queryset)}, status=404, content_type="application/json")
    serializer_class = SMSPriceSerializer


class SMSPriceDetail(generics.RetrieveAPIView):
    """
    This class is responsible for generating, and returning, the view of a single created object of the SMSPrice model.
    It sub-classes the RetrieveDestroyAPIView class of the generics module.
    If it finds the requested object it will return it, but if it doesn't it will return a 404.
    """
    queryset = SMSPrice.objects.all()
    serializer_class = SMSPriceSerializer


class SMSUserCreate(generics.CreateAPIView):
    """
    This class is reponsible for generatng a view for the SMSUser instance creation, aka user registration.
    It sub-classes the CreateAPIView class from the generics module.
    The authentication_classes = () and the permission_classes = () are added to exempt the SMSUserCreate
    class from global authentication scheme.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = SMSUserSerializer


class SMSUserView(generics.ListAPIView):
    """
    This class is responsible for creating a view for the SMSUser model, aka display all the smsuser objects created.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = SMSUserSerializer


class SMSUserUpdate(generics.UpdateAPIView):
    """
    This class is responsible for updating a specific instance of the SMSUser. It sub-classes the UpdateAPIView class
    from the generics module.
    """
    # Every view needs a queryset defined to know what objects to look for. You define the view's queryset by
    # using the queryset attribute (as I suggested) or returning a valid queryset from a get_queryset method. (From S.O)
    # Thus this object that's populated with ClassName.objects.all()

    # TODO: properly document/comment this class
    queryset = SMSUser.objects.all()
    serializer_class = SMSUserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'pk'

    """
    The actual method that does the updating. Overrides the update() method from generics.UpdateAPIView.
    Copied straight outta S.O, question -> https://stackoverflow.com/questions/57306682/how-to-update-a-single-field-in-a-model-using-updateapiview-from-djangorestframe
    """
    # TODO: properly document/comment this method
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.name = request.data.get("name")
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # TODO: write a better Response than this
            return Response({"message": "updated successfully"})
        else:
            # TODO: write a better Response than this
            return Response({"message": "failed", "details": serializer.errors})

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "wrong credentials"}, status=status.HTTP_403_ACCESS_DENIED)
