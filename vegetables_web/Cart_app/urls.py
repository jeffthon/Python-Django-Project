from django.urls import path
from .import views

urlpatterns = [
    path('add/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('summary/',views.cart_summary,name='cart_summary'),
    path('decrease/<int:product_id>/', views.decrease_cart_item, name='decrease_cart_item'),
    path('cart/delete/<int:product_id>/', views.delete_cart_item, name='delete_cart_item'),
]