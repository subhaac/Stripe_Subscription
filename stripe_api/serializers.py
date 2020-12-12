from rest_framework import serializers
from .models import Customer, Payment_Method, Subscription


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_Method
        fields = ("card_type", "card_number", "card_exp_month_year", "card_cvc", "key")


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("username", "payment_method", "key")


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("customer", "key")
