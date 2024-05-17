# stl

# 3rd parties
from rest_framework import serializers
from django.core.validators import RegexValidator


PHONE_VALIDATOR = RegexValidator(
    r"^(\+2517|2517|2519|07|09|\+2519)([0-9]{8})$",
    "The phone number is invalid",
    code="invalid",
)


class PhoneNumberSerializer(serializers.Serializer):
    sms_number_to = serializers.CharField(
        max_length=13, min_length=13, initial="+251", validators=[PHONE_VALIDATOR]
    )
