from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test,login_required
from .Form import ProductForm
from .models import Product
from Farmers_app.models import PersonalData
from django.db.models import Sum

def is_verified_user(user):
    return user.is_authenticated and user.is_verified


def add_product(request):
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product_obj=form.save(commit=False)
            product_obj.farmer=request.user
            product_obj.is_verified=False
            product_obj.save()
            return redirect('personal_data_dashboard')
    else:
        form=ProductForm()
    return render(request,'add_product.html',{'form':form})

def product_list(request):
    # Get all verified products once to save database speed
    all_verified = Product.objects.filter(is_verified=True)

    context = {
        'vegetables': all_verified.filter(category__iexact='vegetables'),
        'fruits': all_verified.filter(category__iexact='fruits'),
        'grains': all_verified.filter(category__iexact='grains'),
    }
    return render(request, 'product_list.html', context)

def home(request):
    featured_products=Product.objects.filter(is_featured=True,is_verified=True)[:4]
    
@login_required
def farmer_journal(request):
    my_products = Product.objects.filter(farmer=request.user)
    special_items = my_products.filter(is_special=True) 
    context = {
        'my_products': my_products,
        'special_items': special_items,
    }
    return render(request, 'farmer_journal.html', context)



