from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from Product_app.models import Product
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction



# Local App Imports
from .Form import UserRegistrationForm, UserRoleForm
from .models import UserRole

# Other App Imports
from Product_app.models import Product  # Correct path
from Product_app.Form import ProductForm

# --- HOME & AUTH ---

def homepage(request):
    featured_items=Product.objects.filter(is_verified=True,is_featured=True).order_by('-id')[:20]
    return render(request,'homepage.html',{'featured_products':featured_items})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if user.is_superuser or user.is_staff:
                return redirect('admin_page') # Ensure this name matches your urls.py
            return redirect('accounts')
        
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'homepage.html')

def user_logout(request):
    logout(request)
    return redirect('homepage')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        role_form = UserRoleForm(request.POST)
        if user_form.is_valid() and role_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            role = role_form.save(commit=False)
            role.user = user
            role.save()
            messages.success(request, "Registration Successful")
            login(request, user)
            return redirect('accounts')
    else:
        user_form = UserRegistrationForm()
        role_form = UserRoleForm()
    return render(request, 'registration.html', {'user_form': user_form, 'role_form': role_form})



def customer_dashboard(request):
    category = request.GET.get('category')
    products = Product.objects.filter(is_verified=True)
    if category:
        products = products.filter(category=category)
    return render(request, 'customer_dashboard.html', {'products': products.order_by('-id')})

@login_required
def farmer_dashboard(request):
    return render(request, 'farmer_dashboard.html')

# --- ADMIN CONTROL PANEL ---

@staff_member_required
def admin_dashboard(request):
    unverified_products = Product.objects.filter(is_verified=False).order_by('-created_at')
    print(f"Pending Products Count: {unverified_products.count()}")
    context = {
        'unverified_products': Product.objects.filter(is_verified=False),
        'verified_products': Product.objects.filter(is_verified=True),
        'pending_farmers': UserRole.objects.filter(role='farmer', is_approved=False),
        'total_farmers': UserRole.objects.filter(role='farmer', is_approved=True).count(),
        'total_customers': UserRole.objects.filter(role='customer').count(),
        'featured_count': Product.objects.filter(is_featured=True).count(), 
    }
    return render(request, 'admin_dashboard.html', context)

@staff_member_required
def toggle_featured(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_featured = not product.is_featured
    product.save()
    return redirect('admin_page') # Redirect back to the dashboard

@staff_member_required
def approve_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.is_verified = True
        product.save()
    return redirect('admin_page')

@staff_member_required # Changed from login_required for security
def approve_farmer(request, role_id):
    if request.method == 'POST':
        role = get_object_or_404(UserRole, id=role_id)
        role.is_approved = True
        role.save()
    return redirect('admin_page')

# --- PRODUCT ACTIONS ---

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, farmer=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.is_verified = False # Require re-verification after edit
            product.save()
            messages.success(request, "Product updated! Awaiting admin re-verification.")
            return redirect('farmer_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, farmer=request.user)
        product.delete()
        messages.success(request, "Product deleted successfully")
    return redirect('farmer_dashboard')



def approve_product(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        with transaction.atomic():
            product.is_verified = True
            product.save()

        
        try:
            send_mail(
                subject="Your Vegetable Listing is Live!",
                message=f"Hi {product.farmer.username}, your product {product.name} has been verified.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[product.farmer.email],
                fail_silently=False, 
            )
            print("--- EMAIL SENT SUCCESSFULLY ---")
        except Exception as e:
            print(f"--- EMAIL ERROR: {e} ---")

    return redirect('admin-page')
