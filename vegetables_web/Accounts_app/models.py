from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FarmerProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    product=models.CharField(max_length=100)
    farm_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class UsersProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField()
    phone=models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class UserRole(models.Model):
    
    Role=(
        ('farmer','Farmer'),
        ('customer','Customer'),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=10,choices=Role)
    is_approved=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
