from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('my-orders/', views.order_history, name='order_history'),
]
