from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from Cart_app.models import CartItem  # Ensure this matches your cart app name
from django.db import transaction
from django.contrib import messages

@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('homepage')
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if not address or not phone:
            messages.error(request, "Please provide address and phone number.")
            return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total_price})
        
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                delivery_address=address,
                phone_number=phone,
                status='Pending',
                is_paid=False
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            cart_items.delete()
        return redirect('initiate_payment', order_id=order.id)
    return render(request, 'checkout.html', {'cart_items': cart_items,'total': total_price})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    pending_orders = orders.filter(status__iexact='pending')
    completed_orders =orders.filter(status__iexact='Delivered')
    processing_orders =orders.filter(status__iexact='processing')
    context = {
        'orders': orders,
        'pending_count': pending_orders.count(),
        'completed_count': completed_orders.count(),
        'processing_count': processing_orders.count(),
    }
    return render(request, 'customer_dashboard.html', context)