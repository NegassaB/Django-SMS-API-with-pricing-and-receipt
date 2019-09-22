from rest_framework import serializers

from commons.models import SMSUser, SMSPrice, Type


class SMSUserSerializer(serializers.ModelSerializer):
    """
    A class for serializing the SMSUser model's data. It sub-classes's the
    ModelSerializer class from serializer's module.
    """

    class Meta:
        model = SMSUser
        fields = 'username, email, first_name, last_name, company_name'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        The method used to create a new SMSUser, (all this is based on the djangoapibook process).
        """
        user = SMSUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            company_name=validated_data['company_name']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SmSPriceSerializer(serializers.ModelSerializer):
    """
    A class for serializing the SMSPrice model's data. It sub-classes's the
    ModelSerializer class from serializer's module.
    """

    class Meta:
        model = SMSPrice
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    """
    A class for serializing the Type model's data. It sub-classes's the
    ModelSerializer class from serializer's module.
    """

    class Meta:
        model = Type
        fields = '__all__'
