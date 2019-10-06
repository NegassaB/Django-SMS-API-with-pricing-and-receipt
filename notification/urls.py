from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from notification.apiviews import SMSendView, SMSMessagesView

app_name = "notification"

router = DefaultRouter()
# router.register('smsmessages', )

urlpatterns = [
    path("smsmessages/", SMSMessagesView.as_view(), name="sms_messages"),
]
