from django import forms
from django.forms import PasswordInput


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password')
    #widgets
    username.widget = forms.TextInput(attrs={'class': 'form-control'})
    password.widget = forms.PasswordInput(attrs={'class': 'form-control'})



class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', widget=PasswordInput())
    email = forms.CharField(label='E-mail', max_length=50)
    img = forms.ImageField(label='Profile Picture')
    phone = forms.CharField(label='Phone Number', max_length=10)
    discord = forms.CharField(label='Discord', max_length=20)
