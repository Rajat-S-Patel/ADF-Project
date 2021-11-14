from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model=Stock
        fields=["ticker","user"] 
