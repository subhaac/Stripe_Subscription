from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.conf import settings
from rest_framework import viewsets
from .models import User_Account, Payment_Method
from .serializers import PaymentMethodSerializer
from datetime import datetime
# Bring in api view, define what to do with POST and GET 

# 1. For a POST request, you need to get the params, card details and user object from the request. 

# 2. You need to make the request to stripe, save the details in your models and do something with the response from Stripe. 

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = Payment_Method.objects.all()
    serializer_class = PaymentMethodSerializer
    
    def create(self, request):
        user = self.request.data['user']
        user_account = User_Account.objects.get(id=user)
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
        print(response.text)

        Payment_Method.objects.create(user=user_account, card_type=card_type, card_number=card_number, card_exp_month_year=card_exp_month_year, card_cvc=card_cvc )

        return HttpResponse(response.text)
        
       
   
    
 
