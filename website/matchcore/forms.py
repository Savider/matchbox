from django import forms
from django.forms import PasswordInput
from . import models


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

class CreateProjectForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
    small_description = forms.CharField(label='Small Description', max_length=100)
    big_description = forms.CharField(label='Big Description', max_length=1000)
    img = forms.ImageField(label='Project Picture')
    theme = forms.ModelChoiceField(queryset=models.ProjectTag.objects.filter(archetype='T'))
    complexity = forms.ModelChoiceField(queryset=models.ProjectTag.objects.filter(archetype='C'))
    technology = forms.ModelChoiceField(queryset=models.ProjectTag.objects.filter(archetype='D'))
    language = forms.ModelChoiceField(queryset=models.ProjectTag.objects.filter(archetype='L'))
