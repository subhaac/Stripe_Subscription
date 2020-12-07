from rest_framework import serializers
from .models import Customer, Payment_Method

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_Method
        fields = ('user', 'card_type', 'card_number', 'card_exp_month_year', 'card_cvc')
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('username',)