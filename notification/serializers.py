# stl

# 3rd parties
from rest_framework import serializers
from django.core.validators import RegexValidator


class PhoneNumberSerializer(serializers.Serializer):
    sms_number_to = serializers.CharField(
        max_length=13, min_length=13, initial="+251", validators=[RegexValidator]
    )
