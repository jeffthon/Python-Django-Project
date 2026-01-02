from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .Form import PersonalDataForm
from .models import PersonalData
from Product_app.models import Product
from django.contrib.auth import logout
from django.contrib import messages
from Product_app.Form import ProductForm

# Create your views here.

def PersonalData_view(request):
    if request.method=='POST':
        form=PersonalDataForm(request.POST,request.FILES)
        if form.is_valid():
            personal=form.save(commit=False)
            personal.user=request.user
            personal.save()
            return redirect('personal_data_dashboard')
    else:
        form=PersonalDataForm()
    return render(request,'personal_data.html',{'form':form})

def farmer_data_dashboard(request):
    personal=PersonalData.objects.filter(user=request.user).first()
    my_products = Product.objects.filter(farmer=request.user).order_by('-id')
    my_products_verified = my_products.filter(is_verified=True)
    context = {
        'personal': personal,
        'my_products': my_products,
        'my_products_verified': my_products_verified,
    }
    return render(request,'farmers_data_dashboard.html',context)

def user_logout(request):
    if request.method=='POST' or request.method=='GET':
        logout(request)
        return redirect('user_login')
    
def edit_product(request, pk):
    
    product = get_object_or_404(Product, pk=pk, farmer=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('farmer_data_dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})
