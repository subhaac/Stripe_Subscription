from django.test import TestCase, RequestFactory
from .models import User_Account, Payment_Method
from datetime import datetime
from .views import PaymentMethodViewSet
from rest_framework.test import APIClient

class StripeTest(TestCase):
    def setUp(self):
        self.factory = APIClient()
        self.user_1 = User_Account.objects.create(username="Peter Parker")
        # self.payment_method_1 = Payment_Method.objects.create(user=self.user_1, card_type="card", card_number="424242424242", card_exp_month_year=datetime(2021,2,2), card_cvc=456)
        
    def test_create_payment_method(self):
        request = self.factory.post('/stripe_api/paymentmethod/', {
            "user": self.user_1.id,
            "card_type": "card",
            "card_number": 424242424242,
            "card_exp_month_year": "2021-02-02",
            "card_cvc": 654,
        }, format='json')
             
        self.assertEqual(request.status_code, 200)