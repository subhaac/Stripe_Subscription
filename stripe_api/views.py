from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.conf import settings
from rest_framework import viewsets
from .models import Customer, Payment_Method, Subscription
from .serializers import (
    PaymentMethodSerializer,
    CustomerSerializer,
    SubscriptionSerializer,
)
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
import stripe


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    # Handle the event
    if event.type == "customer.subscription.created":
        payment_method = event.data.object
        subscription_status = payment_method["items"]["data"][0]["plan"]["active"]
        # Get customer in local db, change subscription status to active
        customer = Customer.objects.get(stripe_customer_id=payment_method["customer"])
        if subscription_status == True:
            customer.status = "Active"
        elif subscription_status == False:
            customer.status = "Inactive"
        customer.save()
    elif event.type == "customer.subscription.updated":
        payment_method = event.data.object
        subscription_status = payment_method["items"]["data"][0]["plan"]["active"]
        # Get customer in local db, change subscription status to active
        customer = Customer.objects.get(stripe_customer_id=payment_method["customer"])
        if subscription_status == True:
            customer.status = "Active"
        elif subscription_status == False:
            customer.status = "Inactive"
        customer.save()
    else:
        print("Unhandled event type {}".format(event.type))
    return HttpResponse(status=200)


def index(request):
    return HttpResponse("Welcome to Stripe Subscription API")


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = Payment_Method.objects.all()
    serializer_class = PaymentMethodSerializer

    def create(self, request):
        card_type = self.request.data["card_type"]
        card_number = self.request.data["card_number"]
        key = self.request.data["key"]

        if key == settings.ACCESS_KEY:
            date_time_str = self.request.data["card_exp_month_year"]

            card_exp_month_year = datetime.strptime(date_time_str, "%Y-%m-%d")

            card_cvc = self.request.data["card_cvc"]

            url = "https://api.stripe.com/v1/payment_methods"

            payload = {
                "type": card_type,
                "card[number]": card_number,
                "card[exp_month]": card_exp_month_year.month,
                "card[exp_year]": card_exp_month_year.year,
                "card[cvc]": card_cvc,
            }
            header = {
                "Authorization": "Bearer " + settings.SECRET_KEY,
                "Content-Type": "application/x-www-form-urlencoded",
            }

            response = requests.post(url, headers=header, params=payload)
            stripe_id = response.json()["id"]

            Payment_Method.objects.create(
                card_type=card_type,
                card_number=card_number,
                card_exp_month_year=card_exp_month_year,
                card_cvc=card_cvc,
                stripe_payment_method_id=stripe_id,
            )

            return HttpResponse("Payment method created!")
        else:
            return HttpResponse("Unauthorized")


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    url = "https://api.stripe.com/v1/customers"
    header = {
        "Authorization": "Bearer " + settings.SECRET_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    def create(self, request):
        customer_name = self.request.data["username"]
        payment_method_id = self.request.data["payment_method"]

        key = self.request.data["key"]

        if key == settings.ACCESS_KEY:
            payment_method = Payment_Method.objects.get(id=payment_method_id)
            # Create Customer and set default payment method
            payload = {
                "description": customer_name,
                "invoice_settings[default_payment_method]": payment_method.stripe_payment_method_id,
                "payment_method": payment_method.stripe_payment_method_id,
            }

            response = requests.post(self.url, headers=self.header, params=payload)
            stripe_customer_id = response.json()["id"]

            customer = Customer.objects.create(
                username=customer_name,
                stripe_customer_id=stripe_customer_id,
                payment_method=payment_method,
            )

            # Attach payment method to customer for future recurring payments.
            # TODO: Change this to use SetupIntent as it's advised in Stripe docs https://stripe.com/docs/api/setup_intents

            attach_payment_method_url = (
                "https://api.stripe.com/v1/payment_methods/"
                + str(payment_method.stripe_payment_method_id)
                + "/attach"
            )

            payload = {
                "customer": customer.stripe_customer_id,
            }

            response = requests.post(
                attach_payment_method_url, headers=self.header, params=payload
            )
            return HttpResponse("Customer created!")
        else:
            return HttpResponse("Unauthorized")


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def create(self, request):
        customer_id = self.request.data["customer"]
        key = self.request.data["key"]

        if key == settings.ACCESS_KEY:
            customer = Customer.objects.get(id=customer_id)
            url = "https://api.stripe.com/v1/subscriptions"
            header = {
                "Authorization": "Bearer " + settings.SECRET_KEY,
                "Content-Type": "application/x-www-form-urlencoded",
            }
            payload = {
                "customer": customer.stripe_customer_id,
                "items[0][price]": "price_1Hvj0CG0xfgwLY2BpeU7unDf",
            }

            response = requests.post(url, headers=header, params=payload)
            subscription_id = response.json()["id"]
            purchase_date = datetime.fromtimestamp(response.json()["start_date"])

            Subscription.objects.create(
                status="Pending",
                purchase_date=purchase_date,
                stripe_subscription_id=subscription_id,
                customer=customer,
                price_id="price_1Hvj0CG0xfgwLY2BpeU7unDf",
            )

            return HttpResponse("Subscription created!")
        else:
            return HttpResponse("Unauthorized")
