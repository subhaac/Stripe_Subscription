from django.contrib import admin
from .models import User_Account, Payment_Method

admin.site.register(User_Account)
admin.site.register(Payment_Method)