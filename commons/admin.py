from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, admin

from commons.forms import CustomUserChangeForm, CustomUserCreationForm
from commons.models import SMSUser, SMSPrice, Type, SMSMessages, Invoice

# Register your models here.


class SMSUserAdmin(UserAdmin):
    """ This class sub-classes the UserAdmin class and is used as a customized admin panel. """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = SMSUser
    list_display = ('username', 'email', 'company_name', 'company_tin')


class SMSMessagesAdmin(admin.ModelAdmin):
    model = SMSMessages
    list_display = ('sms_number_to', 'sms_content', 'sending_user', 'sent_date', 'delivery_status')

""" This registers, aka displays, the models on the admin page. """
admin.site.register(SMSUser, SMSUserAdmin)
admin.site.register(SMSPrice)
admin.site.register(Type)
admin.site.register(SMSMessages, SMSMessagesAdmin)
admin.site.register(Invoice)
