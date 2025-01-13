from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Guest
class LoginForm(forms.Form):
    username=forms.CharField(max_length=20)
    password=forms.CharField(max_length=20,widget=forms.PasswordInput(
        attrs={
            'placeholder':'Enter Password',
        }
    ))


class RegistrationForm(UserCreationForm):
    # confirm_password=forms.CharField(max_length=20,widget=forms.PasswordInput(
    #     attrs={
    #         'placeholder':'Enter Password',
    #     }
    # ))
    class Meta:
        model=Guest
        exclude = ['is_superuser','is_staff',"User permissions"]

