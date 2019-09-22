from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SMSUser, SMSPrice, Type


class CustomUserCreationForm(UserCreationForm):
    """ A form for creating new users. Includes all the required fields. """
    class Meta:
        model = SMSUser
        fields = ('username', 'email', 'company_name')


class CustomUserChangeForm(UserChangeForm):
    """ A form for updating users. Includes all the required fields. """
    class Meta:
        model = SMSUser
        fields = ('username', 'email', 'company_name')
