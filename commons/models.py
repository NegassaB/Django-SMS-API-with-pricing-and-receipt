from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class SMSUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(verbose_name='company email', max_length=254, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=150)
    # make the value 1 in the db an unset value and the rest the actual values
    sms_price = models.ForeignKey("SMSPrice", related_name="sms_prices", on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        verbose_name_plural = "SMSUsers"

    def __str__(self):
        return self.company_name


class SMSPrice(models.Model):
    set_price = models.CharField(max_length=25)
    price_desc = models.CharField(max_length=100)
    # make the value 1 in the db an unset value and the rest the actual values
    type = models.ForeignKey("Type", related_name="types", on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        verbose_name_plural = "SMSPrices"

    def __str__(self):
        return self.price_desc


class Type(models.Model):
    type_of_company = models.CharField(max_length=50)

    def __str__(self):
        return self.type_of_company
