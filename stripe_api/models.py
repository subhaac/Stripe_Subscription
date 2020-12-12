from django.db import models
from fernet_fields import EncryptedTextField


class Payment_Method(models.Model):
    card_type = models.CharField(max_length=50)
    card_number = models.BigIntegerField()
    card_exp_month_year = models.DateField(auto_now=False, auto_now_add=False)
    card_cvc = models.IntegerField()
    stripe_payment_method_id = models.CharField(max_length=50, null=True)
    key = EncryptedTextField()


class Customer(models.Model):
    username = models.CharField(max_length=100)
    stripe_customer_id = models.CharField(max_length=50, null=True)
    payment_method = models.ForeignKey(to=Payment_Method, on_delete=models.CASCADE)
    key = EncryptedTextField()


class Subscription(models.Model):
    status = models.CharField(max_length=50)
    purchase_date = models.DateField(auto_now=False, auto_now_add=False)
    price_id = models.CharField(max_length=50)
    stripe_subscription_id = models.CharField(max_length=50)
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    key = EncryptedTextField()
