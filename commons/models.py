from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class SMSUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=150)
    sms_price = models.ForeignKey("SMSPrice", related_name="sms_prices", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.company_name


class SMSPrice(models.Model):
    set_price = models.CharField(max_length=25)
    price_desc = models.CharField(max_length=100)
    type = models.ForeignKey("Type", related_name="types", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.price_desc


class Type(models.Model):
    type_of_company = models.CharField(max_length=50)

    def __str__(self):
        return self.type_of_company
