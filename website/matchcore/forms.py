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
    nationality = forms.CharField(label='Nationality', max_length=30, required=False)
    img = forms.ImageField(label='Profile Picture', required=False) #required?
    phone = forms.CharField(label='Phone Number', max_length=10, required=False)
    discord = forms.CharField(label='Discord', max_length=20, required=False)
    objective_tag = forms.CharField(max_length=20, widget=forms.HiddenInput())
    expertise_tag = forms.CharField(max_length=20, widget=forms.HiddenInput())
    #widgets
    username.widget = forms.TextInput(attrs={'class': 'form-control register-input r-req'})
    password.widget = forms.PasswordInput(attrs={'class': 'form-control register-input r-req'})
    email.widget = forms.EmailInput(attrs={'class': 'form-control register-input r-req'})
    nationality.widget = forms.TextInput(attrs={'class': 'form-control register-input'})
    phone.widget = forms.NumberInput(attrs={'class': 'form-control register-input'})
    discord.widget = forms.TextInput(attrs={'class': 'form-control register-input'})


class ProfileUpdateForm(forms.Form):
    email = forms.CharField(label='E-mail', max_length=50)
    img = forms.ImageField(label='Profile Picture')
    nationality = forms.CharField(label='Nationality', max_length=20, required=False)
    phone = forms.CharField(label='Phone Number', max_length=10, required=False)
    discord = forms.CharField(label='Discord', max_length=20, required=False)
    #widgets
    email.widget = forms.TextInput(attrs={'class': 'form-control'})
    nationality.widget = forms.TextInput(attrs={'class': 'form-control'})
    phone.widget = forms.NumberInput(attrs={'class': 'form-control'})
    discord.widget = forms.TextInput(attrs={'class': 'form-control'})


class CreateProjectForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
    small_description = forms.CharField(label='Small Description', max_length=100)
    big_description = forms.CharField(label='Big Description', max_length=1000)
    img = forms.ImageField(label='Project Picture')
    theme = forms.ModelChoiceField(queryset=models.ProjectTag.objects.filter(archetype='T'))
    complexity = forms.ModelChoiceField(queryset=models.ProjectTag.objects.filter(archetype='C'))
    technology = forms.ModelChoiceField(queryset=models.ProjectTag.objects.filter(archetype='D'))
    language = forms.ModelChoiceField(queryset=models.ProjectTag.objects.filter(archetype='L'))
    #widgets
    title.widget = forms.TextInput(attrs={'class': 'form-control'})
    small_description.widget = forms.TextInput(attrs={'class': 'form-control'})
    big_description.widget = forms.Textarea(attrs={'class': 'form-control'})


class EvaluateForm(forms.Form):
    name = forms.CharField(label='Username', max_length=20, widget=forms.HiddenInput())
    contribution = forms.IntegerField(label='Evaluation')