from django.contrib import admin
from .models import Customer, Payment_Method, Subscription

admin.site.register(Customer)
admin.site.register(Payment_Method)
admin.site.register(Subscription)
