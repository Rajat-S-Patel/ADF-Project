from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import fields

from .models import CustomUser

class RegisterForm(UserCreationForm):
    
    username=forms.CharField(label='Username',max_length=100,widget=forms.TextInput())
    email=forms.EmailField(label='Email',max_length=100,widget=forms.EmailInput())
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields=('username','email','password1','password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username',max_length=100,widget=forms.TextInput())
    password = forms.CharField(label='Password',widget=forms.PasswordInput())

    class Meta:
        fields=('username','password')

class PersonalInfoUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name',max_length=100,widget=forms.TextInput())
    last_name = forms.CharField(label='Last Name',max_length=100,widget=forms.TextInput())
    image = forms.ImageField(label='Profile Picture',required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','image')

