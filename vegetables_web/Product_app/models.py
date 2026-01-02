from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight_or_qty = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, help_text="Check this to show on Home Page Featured section")
  


    CATEGORY_CHOICES = [
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('grains', 'Grains & Pulses'),
        
    ]
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='vegetables'
    )
    
    def __str__(self):
        return f"{self.name} - {'Verified' if self.is_verified else 'Pending'}"