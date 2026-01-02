from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import PersonalData

class PersonalDataForm(forms.ModelForm):
    class Meta:
        model=PersonalData
        exclude=[
          'user',
          'Is_verified',
          'created_at',
          'Updated_at',
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Full Name'}),
            'VegetableName': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Main Crop (e.g. Tomato)'}),
            'Phone': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Phone Number'}),
            'Address': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Full Address', 'rows': 3}),
            'Email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email Address'}),
            'District': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'District'}),
            'state': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Pincode'}),
            'Id_proof': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'ID Type (Aadhar/Voter)'}),
            'Id_number': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'ID Number'}),
        }