from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Product

@admin.action(description="Approve selected products")
def make_approved(modeladmin, request, queryset):
    queryset.update(is_verified=True) 
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'farmer', 'price', 'stock', 'is_verified', 'is_featured']
    list_filter = ['is_verified', 'is_featured']
    list_editable = ['is_verified', 'is_featured']
    search_fields = ['name']
    
    actions = [make_approved]


