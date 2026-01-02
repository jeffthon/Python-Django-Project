from django.db import models
from django.db import models
from django.conf import settings
from Product_app.models import Product 

class Order(models.Model):
    STATUS_CHOICES = (
        ('Processing','Processing'),
        ('Pending','Pending'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    delivery_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    stock_updated = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
    @property
    def get_cart_total(self):
        orderitems = self.items.all()
        total = sum([item.get_total_item_price() for item in orderitems])
        return total

class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    def get_total_item_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
