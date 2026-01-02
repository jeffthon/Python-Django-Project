from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from Orders_app.models import Order


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    
    amount = int(order.total_price * 100)
    
    
    data = {
        "amount": amount,
        "currency": "INR",
        "receipt": f"order_rcptid_{order.id}"
    }
    razorpay_order = client.order.create(data=data)
    
    
    context = {
        'order': order,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'amount': amount,
        'callback_url':f"http://127.0.0.1:8000/payment/verify-payment/{order.id}/"
    }
    return render(request, 'payment.html', context)

@csrf_exempt
def verify_payment(request, order_id):
    if request.method == "POST":
        
        payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            
            client.utility.verify_payment_signature(params_dict)
            order = Order.objects.get(id=order_id)
            order.is_paid = True
            order.status = 'Processing'
            order.save()
            return render(request, 'payment_success.html',{'order':order})
        except:
            return render(request, 'payment_failed.html')
