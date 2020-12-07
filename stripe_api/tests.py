from django.test import TestCase, RequestFactory
from .models import Customer, Payment_Method
from datetime import datetime
from .views import PaymentMethodViewSet
from rest_framework.test import APIClient

class StripeTest(TestCase):
    def setUp(self):
        self.factory = APIClient()
        self.user_1 = Customer.objects.create(username="Peter Parker")
    
    def test_create_payment_method(self):
        request = self.factory.post('/stripe_api/paymentmethod/', {
            "user": self.user_1.id,
            "card_type": "card",
            "card_number": 424242424242,
            "card_exp_month_year": "2021-02-02",
            "card_cvc": 654,
        }, format='json')
             
        self.assertEqual(request.status_code, 200)
        
    def test_create_customer(self):
        request = self.factory.post('/stripe_api/customer/', {
            "username": "test_user",
        }, format='json')
        
        self.assertEqual(request.status_code, 200)