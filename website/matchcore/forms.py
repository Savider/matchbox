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

    #widgets
    username.widget = forms.TextInput(attrs={'class': 'form-control register-input'})
    password.widget = forms.PasswordInput(attrs={'class': 'form-control register-input'})
    email.widget = forms.EmailInput(attrs={'class': 'form-control register-input'})
    phone.widget = forms.NumberInput(attrs={'class': 'form-control register-input'})
    discord.widget = forms.EmailInput(attrs={'class': 'form-control register-input'})
