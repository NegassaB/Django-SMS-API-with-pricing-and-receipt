from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from commons.forms import CustomUserChangeForm, CustomUserCreationForm
from commons.models import SMSUser, SMSPrice, Type, SMSMessages, Invoice

# Register your models here.


class SMSUserAdmin(UserAdmin):
    """This class sub-classes the UserAdmin class and is used as a customized admin panel."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = SMSUser
    list_display = (
        "username",
        "email",
        "company_name",
        "company_tin",
        "company_status",
    )

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return Exception("no permission to access this object")
        return super(SMSUserAdmin, self).get_queryset(request)


class SMSMessagesAdmin(admin.ModelAdmin):
    model = SMSMessages
    list_display = (
        "sms_number_to",
        "sms_content",
        "sending_user",
        "sent_date",
        "delivery_status",
    )

    def get_queryset(self, request):
        qs = super(SMSMessagesAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(sending_user=request.user)


""" This registers, aka displays, the models on the admin page. """
admin.site.register(SMSUser, SMSUserAdmin)
admin.site.register(SMSPrice)
admin.site.register(Type)
admin.site.register(SMSMessages, SMSMessagesAdmin)
admin.site.register(Invoice)
