from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import FarmerProfile,UsersProfile,UserRole

class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model=User
        fields=['username','email','password']
        
        def clean(self):
            cleaned_data=super().clean()
            password=cleaned_data.get("password")
            confirm_password=cleaned_data.get("confirm_password")
            if password != confirm_password:
                raise forms.ValidationError("password do not match")
            return cleaned_data
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UsersProfile
        fields=['address','phone']
    
class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model=FarmerProfile
        fields=['product','farm_name','phone']

class UserRoleForm(forms.ModelForm):
    class Meta:
        model=UserRole
        fields=['role']
class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'Placeholder':'username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))