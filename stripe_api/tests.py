from django.test import TestCase, RequestFactory
from .models import Customer, Payment_Method, Subscription
from datetime import datetime
from .views import PaymentMethodViewSet, my_webhook_view
from rest_framework.test import APIClient
import json
from unittest.mock import Mock, patch
import requests
from django.urls import reverse
from requests.models import Response
import stripe


class StripeTest(TestCase):
    def setUp(self):
        self.factory = APIClient()

    def test_create_payment_method(self):
        with patch("requests.post") as mock_request:

            the_response = Response()
            the_response.status_code = 200
            the_response._content = b'{ "id" : "test_payment_method_1" }'

            mock_request.return_value = the_response

            request = self.factory.post(
                "/stripe_api/paymentmethod/",
                {
                    "card_type": "card",
                    "card_number": 4242424242424242,
                    "card_exp_month_year": "2061-10-06",
                    "card_cvc": 189,
                },
                format="json",
            )
            self.assertEqual(request.status_code, 200)
            self.assertEqual(request._container[0], b"Payment method created!")

            payment_method = Payment_Method.objects.get(card_cvc=189)
            self.assertEqual(
                payment_method.stripe_payment_method_id, "test_payment_method_1"
            )
            self.assertEqual(payment_method.card_cvc, 189)

    def test_create_customer(self):

        with patch("requests.post") as mock_request:

            the_response = Response()
            the_response.status_code = 200
            the_response._content = b'{ "id" : "test_payment_method_2" }'

            mock_request.return_value = the_response

            request = self.factory.post(
                "/stripe_api/paymentmethod/",
                {
                    "card_type": "card",
                    "card_number": 4242424242424242,
                    "card_exp_month_year": "2061-10-06",
                    "card_cvc": 256,
                },
                format="json",
            )
            self.assertEqual(request.status_code, 200)
            self.assertEqual(request._container[0], b"Payment method created!")

            payment_method = Payment_Method.objects.get(card_cvc=256)
            self.assertEqual(
                payment_method.stripe_payment_method_id, "test_payment_method_2"
            )
            self.assertEqual(payment_method.card_cvc, 256)

        with patch("requests.post") as mock_request:
            the_response = Response()
            the_response.status_code = 200
            the_response._content = b'{ "id" : "test_customer_1" }'
            mock_request.return_value = the_response

            request = self.factory.post(
                "/stripe_api/customer/",
                {
                    "username": "test_create_customer",
                    "payment_method": payment_method.id,
                },
                format="json",
            )
            self.assertEqual(request.status_code, 200)
            self.assertEqual(request._container[0], b"Customer created!")

            customer = Customer.objects.get(username="test_create_customer")
            self.assertEqual(customer.stripe_customer_id, "test_customer_1")
            self.assertEqual(
                customer.payment_method.stripe_payment_method_id,
                "test_payment_method_2",
            )

    def test_create_subscription(self):
        with patch("requests.post") as mock_request:
            the_response = Response()
            the_response.status_code = 200
            the_response._content = b'{ "id" : "test_payment_method_3" }'
            mock_request.return_value = the_response
            request = self.factory.post(
                "/stripe_api/paymentmethod/",
                {
                    "card_type": "card",
                    "card_number": 4242424242424242,
                    "card_exp_month_year": "2021-02-02",
                    "card_cvc": 789,
                },
                format="json",
            )
            payment_method = Payment_Method.objects.get(card_cvc=789)
            self.assertEqual(request.status_code, 200)
            self.assertEqual(request._container[0], b"Payment method created!")

            self.assertEqual(
                payment_method.stripe_payment_method_id, "test_payment_method_3"
            )
            self.assertEqual(payment_method.card_cvc, 789)

        with patch("requests.post") as mock_request:
            the_response = Response()
            the_response.status_code = 200
            the_response._content = b'{ "id" : "test_customer_2" }'
            mock_request.return_value = the_response

            request = self.factory.post(
                "/stripe_api/customer/",
                {"username": "test_user_2", "payment_method": payment_method.id},
                format="json",
            )

            self.assertEqual(request.status_code, 200)
            self.assertEqual(request._container[0], b"Customer created!")

            user = Customer.objects.get(username="test_user_2")
            self.assertEqual(user.stripe_customer_id, "test_customer_2")
            self.assertEqual(
                user.payment_method.stripe_payment_method_id, "test_payment_method_3"
            )

        with patch("requests.post") as mock_request:
            the_response = Response()
            the_response.status_code = 200
            the_response._content = b'{ "id" : "subscription_1", "status": "Active", "start_date": 1607780012 }'
            mock_request.return_value = the_response

            request_to_create_subscription = self.factory.post(
                "/stripe_api/subscription/",
                {
                    "customer": user.id,
                },
                format="json",
            )

            self.assertEqual(request_to_create_subscription.status_code, 200)
            self.assertEqual(
                request_to_create_subscription._container[0], b"Subscription created!"
            )

            subscription = Subscription.objects.get(customer=user)
            self.assertEqual(subscription.customer.id, user.id)
            self.assertEqual(subscription.status, "Pending")

    def test_webhook(self):
        with patch("requests.post") as mock_request:
            the_response = Response()
            the_response.status_code = 200
            the_response._content = b'{ "id" : "test_payment_method_3" }'
            mock_request.return_value = the_response
            request = self.factory.post(
                "/stripe_api/paymentmethod/",
                {
                    "card_type": "card",
                    "card_number": 4242424242424242,
                    "card_exp_month_year": "2021-02-02",
                    "card_cvc": 789,
                },
                format="json",
            )
            payment_method = Payment_Method.objects.get(card_cvc=789)
            self.assertEqual(request.status_code, 200)
            self.assertEqual(request._container[0], b"Payment method created!")

            self.assertEqual(
                payment_method.stripe_payment_method_id, "test_payment_method_3"
            )
            self.assertEqual(payment_method.card_cvc, 789)

        with patch("requests.post") as mock_request:
            the_response = Response()
            the_response.status_code = 200
            the_response._content = b'{ "id" : "test_customer_4" }'
            mock_request.return_value = the_response

            request = self.factory.post(
                "/stripe_api/customer/",
                {"username": "test_user_2", "payment_method": payment_method.id},
                format="json",
            )

            self.assertEqual(request.status_code, 200)
            self.assertEqual(request._container[0], b"Customer created!")

            user = Customer.objects.get(username="test_user_2")
            self.assertEqual(user.stripe_customer_id, "test_customer_4")
            self.assertEqual(
                user.payment_method.stripe_payment_method_id, "test_payment_method_3"
            )

        with patch("stripe.Event.construct_from") as mock_request:
            mock_request.type = "test"

        webhook_sample_payload = json.dumps(
            {
                "data": {
                    "object": {
                        "items": {"data": [{"plan": {"active": True}}]},
                        "customer": "test_customer_4",
                    }
                },
                "type": "customer.subscription.created",
            }
        )
        mock_request_2 = Mock()
        mock_request_2.body = webhook_sample_payload

        response = my_webhook_view(mock_request_2)
        self.assertEqual(response.status_code, 200)
