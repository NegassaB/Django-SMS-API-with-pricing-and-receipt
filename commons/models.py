from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

# Create your models here.


class SMSUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(verbose_name='company email', max_length=254, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=150)
    # make the value 1 in the db an unset value and the rest the actual values
    sms_price = models.ForeignKey("SMSPrice", related_name="sms_prices", on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "SMSUsers"

    def __str__(self):
        return self.company_name


class SMSPrice(models.Model):
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
In the below model I used the usr foreign key to link it to the SMSuser that sent the message. In the proceeding logic
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
