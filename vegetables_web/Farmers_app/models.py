from django.db import models
from django.contrib.auth.models import User


class PersonalData(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    name=models.CharField(max_length=50)
    VegetableName=models.CharField(max_length=50)
    Phone=models.CharField(max_length=15)
    Address=models.TextField()
    Email=models.EmailField()
    District=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    pincode=models.CharField(max_length=6)
    Id_proof=models.CharField(max_length=50)
    Id_number=models.CharField(max_length=50)
    Profile_photo = models.ImageField(upload_to='farmers/profiles/', blank=True, null=True)
    
    Is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name