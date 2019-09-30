"""
The acutal urls.py file that will do most of the work.
"""
from django.urls import path, include
from rest_framework.authtoken import views

# if you need a custom login, you can import LoginView and LoginView.as_view() in the path
from commons.apiviews import TypeList, TypeDetail, SMSPriceList, SMSPriceDetail, SMSUserCreate, SMSUserUpdate
from .views import homepage
"""
describe the entire urlpattern here.
"""

app_name = "commons"

urlpatterns = [
    # for the homepage view, strictly html
    path("", homepage, name="homepage"),
    # for all the types of sms users presented as_view()
    path("types/", TypeList.as_view(), name="type_list"),
    # for a specific type of sms users presented as_view()
    path("types/<int:pk>/", TypeDetail.as_view(), name="type_details"),
    # for all the prices of sms presented as_view()
    path("prices/", SMSPriceList.as_view(), name="price_list"),
    # for a specific price of sms users presented as_view()
    path("prices/<int:pk>/", SMSPriceDetail.as_view(), name="price_details"),
    # for all the sms users presented as_view()
    path("smsusers/", SMSUserCreate.as_view(), name="create_sms_user"),
    # for updating a specific smsuser presented as_view()
    path("smsusers/update/<int:pk>/", SMSUserUpdate.as_view(), name="update_sms_user"),
    # for logining in a user by obtaining an authorization token
    path("login/", views.obtain_auth_token, name="login"),
]
