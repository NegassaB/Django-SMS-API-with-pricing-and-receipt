from rest_framework import serializers
from rest_framework.authtoken.models import Token

from commons.models import SMSUser, SMSPrice, Type, SMSMessages, Invoice


class SMSUserSerializer(serializers.ModelSerializer):
    """
    A class for serializing the SMSUser model's data. It sub-classes's the
    ModelSerializer class from serializer's module.
    """
    class Meta:
        """
        This Meta class defines what must be included in the fields when a post request is made
        (everything but the sms_price), and makes sure that the password is not returned in the response
        by using the extra_kwargs to set the password field to write_only.
        """
        model = SMSUser
        exclude = ('sms_price', )
        # fields = ('username, email, first_name, last_name, company_name, password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        The method used to create a new SMSUser, (all this is based on the djangoapibook process).
        It also includes a way to create an authorization Token for the created user.
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
        Token.objects.create(user=user)
        return user


class TypeSerializer(serializers.ModelSerializer):
    """
    A class for serializing the Type model's data. It sub-classes's the
    ModelSerializer class from serializer's module.
    """

    class Meta:
        model = Type
        fields = '__all__'


class SMSPriceSerializer(serializers.ModelSerializer):
    """
    A class for serializing the SMSPrice model's data. It sub-classes's the
    ModelSerializer class from serializer's module.
    """

    types = TypeSerializer(many=True, read_only=True)

    class Meta:
        model = SMSPrice
        fields = '__all__'


class SMSMessagesSerializer(serializers.ModelSerializer):
    """
    A class for serializing the SMSMessages model's data. It sub-classes the
    ModelSerializer class from serializer's module.
    """

    class Meta:
        model = SMSMessages
        fields = '__all__'

        def update(self, instance, validated_data):
            """
            This method is used to update an instance of the SMSMessages's delivery_status attribute.
            It get's the value for delivery_status from the input parameter, updates the specific instance
            of the SMSMessagesSerializer, saves that instance and returns it.
            """
            instance = self.get_object()
            instance.delivery_status = validated_data.get('delivery_status', instance.delivery_status)
            # checks if the instance is valid before saving it into db, don't know what happens if it fails tho
            if instance.is_valid():
                instance.save()
            return instance


class InvoiceSerialzer(serializers.ModelSerializer):
    """
    A class for serializing the Invoice model's data. It sub-classes the
    ModelSerializer class from serializer's module.
    """

    class Meta:
        model = Invoice
        fields = '__all__'


    def create(self, validated_data):
        """
        The method used to create a new Invoice, (all this is based on the djangoapibook process).
        """
        user_invoice = Invoice(invoice_to=validated_data['username'])
        return user_invoice


    def update(self, instance, validated_data):
        """
        This method is used to update an instance of the Invoice payment_status attribute.
        It get's the value for payment_status from the input parameter, updates the specific instance
        of the InvoiceSerializer, saves that instance and returns it.
        """
        instance = self.get_object()
        instance.payment_status = validated_data.get('payment_status', instance.payment_status)
        # checks if the instance is valid before saving it into db, don't know what happens if it fails tho
        if instance.is_valid():
            instance.save()
        return instance
