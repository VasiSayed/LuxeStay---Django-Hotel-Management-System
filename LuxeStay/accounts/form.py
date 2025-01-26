from django import forms

from django.contrib.auth.forms import UserCreationForm,PasswordResetForm,SetPasswordForm
from .models import Guest


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'form-control',
            'placeholder': 'Enter your email',
        }),
    )

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Enter your new password',
        }),
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'Confirm your new password',
        }),
    )

    field_order = ['new_password1', 'new_password2']



class LoginForm(forms.Form):
    username=forms.CharField(max_length=20)
    password=forms.CharField(max_length=20,widget=forms.PasswordInput(
        attrs={
            'placeholder':'Enter Password',
        }
    ))


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Guest
        exclude = ['is_superuser', 'is_staff', 'user_permissions', 'groups', 'is_active', 'date_joined', 'last_login']
        fields = ['username', 'first_name', 'last_name', 'email', 'contact_details', 'd_o_b', 'gender']



class ChangePasswordFOrm(forms.Form):
    Current_Password=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={
         'placeholder':'Enter Password',
    }))
    New_Password=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={
         'placeholder':'Enter Password',
    }))
    Comfirm_Password=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={
         'placeholder':'Enter Password',
    }))