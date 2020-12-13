from rest_framework import serializers
from .models import Customer, Payment_Method, Subscription


class PaymentMethodSerializer(serializers.ModelSerializer):
    card_exp_month_year = serializers.DateField(format="%Y-%m")
    class Meta:
        model = Payment_Method
        fields = ("id","card_type", "card_number", "card_exp_month_year", "card_cvc")
        # TODO: hide card details

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "username", "payment_method")


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("id", "customer")
