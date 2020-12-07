from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.conf import settings
from rest_framework import viewsets
from .models import Customer, Payment_Method
from .serializers import PaymentMethodSerializer, CustomerSerializer
from datetime import datetime
# Bring in api view, define what to do with POST and GET 

# 1. For a POST request, you need to get the params, card details and user object from the request. 

# 2. You need to make the request to stripe, save the details in your models and do something with the response from Stripe. 
def index(request):
    return HttpResponse("Welcome to Stripe Subscription API")

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = Payment_Method.objects.all()
    serializer_class = PaymentMethodSerializer
    
    def create(self, request):
        card_type = self.request.data['card_type']
        card_number = self.request.data['card_number']
        
        date_time_str = self.request.data['card_exp_month_year']
        
        card_exp_month_year = datetime.strptime(date_time_str, '%Y-%m-%d')
        
        card_cvc = self.request.data['card_cvc']
        
        url = "https://api.stripe.com/v1/payment_methods"
        
        payload = {
            "type": card_type,
            "card[number]" : card_number,
            "card[exp_month]" : card_exp_month_year.month,
            "card[exp_year]" : card_exp_month_year.year,
            "card[cvc]" : card_cvc,
        }
        header = {
            "Authorization": "Bearer " + settings.SECRET_KEY,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(url, headers=header, params=payload)
        
        Payment_Method.objects.create(card_type=card_type, card_number=card_number, card_exp_month_year=card_exp_month_year, card_cvc=card_cvc, stripe_payment_method_id=response.json()["id"])

        return HttpResponse(response.text)
        
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def create(self, request):
        customer_name = self.request.data['username']
        payment_method_id = self.request.data['payment_method']
        payment_method = Payment_Method.objects.get(id=payment_method_id)
        url = "https://api.stripe.com/v1/customers"
        
        payload = {
            "description": customer_name,
        }
        header = {
            "Authorization": "Bearer " + settings.SECRET_KEY,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(url, headers=header, params=payload)
        Customer.objects.create(username=customer_name, stripe_customer_id=response.json()["id"], payment_method=payment_method)

        return HttpResponse(response.text)
       
   
    
 
