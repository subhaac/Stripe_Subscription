from django.test import TestCase, RequestFactory
from .models import Customer, Payment_Method
from datetime import datetime
from .views import PaymentMethodViewSet
from rest_framework.test import APIClient
import json

class StripeTest(TestCase):
    def setUp(self):
        self.factory = APIClient()
        
    def test_create_payment_method(self):
        request = self.factory.post('/stripe_api/paymentmethod/', {
            "card_type": "card",
            "card_number": 4242424242424242,
            "card_exp_month_year": "2051-11-05",
            "card_cvc": 159,
        }, format='json')
        self.assertEqual(request.status_code, 200)
        
        
    def test_create_customer(self):
        request = self.factory.post('/stripe_api/paymentmethod/', {
            "card_type": "card",
            "card_number": 4242424242424242,
            "card_exp_month_year": "2061-10-06",
            "card_cvc": 189,
        }, format='json')
        self.assertEqual(request.status_code, 200)
        
        payment_method = Payment_Method.objects.get(card_cvc=189)
        
        request = self.factory.post('/stripe_api/customer/', {
            "username": "test_create_customer",
            "payment_method": payment_method.id
        },format='json')
        
        self.assertEqual(request.status_code, 200)
        
    def test_create_subscription(self):
        request = self.factory.post('/stripe_api/paymentmethod/', {
            "card_type": "card",
            "card_number": 4242424242424242,
            "card_exp_month_year": "2021-02-02",
            "card_cvc": 654,
        }, format='json')
        payment_method = Payment_Method.objects.get(card_cvc=654)
        self.assertEqual(request.status_code, 200)
        

        request = self.factory.post('/stripe_api/customer/', {
            "username": "test_user",
            "payment_method": payment_method.id
        },format='json')
        
        self.assertEqual(request.status_code, 200)
        
        user = Customer.objects.get(username="test_user")
        
        request_to_create_subscription = self.factory.post('/stripe_api/subscription/', {
            "customer" : user.id,
        },format='json')
        
        self.assertEqual(request.status_code, 200)