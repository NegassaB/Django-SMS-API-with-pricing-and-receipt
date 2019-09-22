from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SMSUser, SMSPrice, Type


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = SMSUser
        fields = ('username', 'email', 'company_name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = SMSUser
        fields = ('username', 'email', 'company_name')
