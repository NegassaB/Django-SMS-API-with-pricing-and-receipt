from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from commons.forms import CustomUserChangeForm, CustomUserCreationForm
from commons.models import SMSUser, SMSPrice, Type, SMSMessages

# Register your models here.


class SMSUserAdmin(UserAdmin):
    """ This class sub-classes the UserAdmin class and is used as a customized admin panel. """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = SMSUser
    list_display = ('username', 'email', 'company_name')

""" This registers, aka displays, the models on the admin page. """
admin.site.register(SMSUser, SMSUserAdmin)
admin.site.register(SMSPrice)
admin.site.register(Type)
admin.site.register(SMSMessages)
