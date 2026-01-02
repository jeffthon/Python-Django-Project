from django.shortcuts import redirect,get_object_or_404,render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem
from Product_app.models import Product
from django.contrib.auth.models import User
from django.db.models import Sum



def add_to_cart(request,product_id):
    
    if request.user.is_authenticated:
        product=get_object_or_404(Product,id=product_id)
        cart_item,created=CartItem.objects.get_or_create(user=request.user,product=product)
        if not created:
            cart_item.quantity +=1
            cart_item.save()
            messages.success(request,f"Increased quantityof  {product.name}")
        else:
            messages.success(request,f"{product.name} added to your basket")
        return redirect(request.META.get('HTTP_REFERER', 'product_list'))
    else:
        return redirect('/?openLogin=true')
   

@login_required
def cart_summary(request):
    items=CartItem.objects.filter(user=request.user)
    grand_total=sum(item.product.price*item.quantity for item in items)
    return render(request,'cart_summary.html',{'items':items,'grand_total':grand_total})

@login_required
def decrease_cart_item(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'cart_summary'))


def marketplace(request):
    vegetables = Product.objects.filter(category='vegetables')
    fruits = Product.objects.filter(category='fruits')
    grains = Product.objects.filter(category='grains')
    
    total_quantity = 0
    if request.user.is_authenticated:
        result = request.user.cartitem_set.aggregate(total=Sum('quantity'))
        total_quantity = result['total'] or 0

    return render(request, 'marketplace.html', {
        'vegetables': vegetables,
        'fruits': fruits,
        'grains': grains,
        'total_quantity': total_quantity,
    })

@login_required
def delete_cart_item(request,product_id):
    cart_item=get_object_or_404(CartItem,user=request.user,product_id=product_id)
    product_name=cart_item.product.name
    cart_item.delete()
    messages.success(request,f"Removed {product_name} from your basket")
    return redirect('cart_summary')