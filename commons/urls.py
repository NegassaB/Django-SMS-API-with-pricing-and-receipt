"""
The acutal urls.py file that will do most of the work.
"""
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

# if you need a custom login, you can import LoginView and LoginView.as_view() in the path
from commons.apiviews import TypeList, TypeDetail, SMSPriceList, SMSPriceDetail, SMSUserCreate, SMSUserUpdate, SMSUserViewSet, LoginView, LogoutView

"""
describe the entire urlpattern here.
"""

app_name = "commons"

router = DefaultRouter()
router.register('smsusers', SMSUserViewSet, base_name="smsusers")

urlpatterns = [
    # for all the types of sms users, presented as_view()
    path('types/', TypeList.as_view(), name="type_list"),
    # for a specific type of sms users, presented as_view()
    path('types/<int:pk>/', TypeDetail.as_view(), name="type_details"),
    # for all the prices of sms, presented as_view()
    path('prices/', SMSPriceList.as_view(), name="price_list"),
    # for a specific price of sms users, presented as_view()
    path('prices/<int:pk>/', SMSPriceDetail.as_view(), name="price_details"),
    # for the sms users creation, presented as_view()
    path('smsusers/create/', SMSUserCreate.as_view(), name="create_sms_user"),
    # for updating a specific smsuser, presented as_view()
    path('smsusers/update/<int:pk>/', SMSUserUpdate.as_view(), name="update_sms_user"),
    # for displaying all the instances of smsuser, presented as_view()
    # path("smsusers/", SMSUserViewSet, name="view_all_sms_users"),
    # for loging in using the LoginView
    path('login/', LoginView.as_view(), name="login"),
    # for logining in a user by using DRF to obtain an authorization token
    # path('login/', views.obtain_auth_token, name="login"),
    # for logging out a user by deleting authorization token
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls
