from django.contrib import admin
from django.urls import path, include
from django.conf import urls 
from stripe_api import views
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'paymentmethod', views.PaymentMethodViewSet)
router.register(r'customer', views.CustomerViewSet)
router.register(r'subscription', views.SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]