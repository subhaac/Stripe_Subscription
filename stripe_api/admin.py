from django.contrib import admin
from .models import Customer, Payment_Method

admin.site.register(Customer)
admin.site.register(Payment_Method)