from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

from django.core.validators import RegexValidator

# Create your models here.


class SMSUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(verbose_name='company email', max_length=254, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=150)
    # make the value 1 in the db an unset value and the rest the actual values
    sms_price = models.ForeignKey("SMSPrice", related_name="sms_prices", on_delete=models.PROTECT, default=1)
    # since an Integer field will not let us use 0 and have a max_length, the validator below will
    # kick in and make sure only number's are put in here.
    company_tin = models.CharField(max_length=10, default=1, validators=[RegexValidator(r'^\d{1, 10}$')])
    # TODO right before production, change this to False as to not fuck yourself
    company_status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "SMSUsers"

    def __str__(self):
        return self.username


class SMSPrice(models.Model):
    # change to floatField
    set_price = models.CharField(max_length=25)
    price_desc = models.CharField(max_length=100)
    # make the value 1 in the db an unset value and the rest the actual values
    type = models.ForeignKey("Type", related_name="types", on_delete=models.PROTECT, related_query_name="SMSPrices")

    class Meta:
        verbose_name_plural = "SMSPrices"

    def __str__(self):
        return self.price_desc


class Type(models.Model):
    type_of_company = models.CharField(max_length=50)

    def __str__(self):
        return self.type_of_company


"""
In the below model I used the user foreign key to link it to the SMSuser that sent the message. In the proceeding logic
before sending it to ethio-telecom's api use this foreign key to derive the user token and the messaging company.
Btw I have decided to leave the msg_key attribute to the login info and have it transfered via the authorization header.
"""


class SMSMessages(models.Model):
    sms_number_to = models.CharField(max_length=14)
    sms_content = models.CharField(max_length=160)
    sending_user = models.ForeignKey("SMSUser", on_delete=models.PROTECT, related_name="user_that_sent")
    sent_date = models.DateTimeField(auto_now=True)
    delivery_status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "SMSMessages"

    def __str__(self):
        return str(self.sending_user)


"""
A class to track the invoices generated. It has all the necessary infos. But perhaps, I might
need to add the actual file generated here. Time will tell.
"""
class Invoice(models.Model):
    # invoice_number = models.CharField(max_length=10, default=1, validators=[RegexValidator(r'^\d{1, 10}$')], primary_key=True)
    invoice_to = models.ForeignKey("SMSUser", related_name="invoiced_user", on_delete=models.PROTECT, related_query_name="invoiced_user")
    payment_status = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = "Invoices"
    

    def __str__(self):
        return str(self.invoice_to) + str(self.payment_status)
