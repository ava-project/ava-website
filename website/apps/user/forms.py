from django import forms
from django.contrib.auth.models import User

from .validators import UsernameValidator, emailUniqueValidator


class RegisterForm(forms.ModelForm):
    email = forms.CharField(
        max_length=75,
        validators=[emailUniqueValidator],
        required=True
    )
    username = forms.CharField(
        max_length=75,
        validators=[UsernameValidator()],
        required=True
    )
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
