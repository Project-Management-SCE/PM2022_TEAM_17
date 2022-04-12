from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateNewAgent(UserCreationForm):
    nameInput = forms.CharField()
    cityInput = forms.CharField()
    mobileInput = forms.CharField()
    emailInput = forms.EmailField()
    inputPassword = forms.PasswordInput()
