from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('pay/<int:order_id>/', views.initiate_payment, name='initiate_payment'),
    path('verify-payment/<int:order_id>/', views.verify_payment, name='verify_payment'),
]