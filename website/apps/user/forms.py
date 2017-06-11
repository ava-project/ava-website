from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

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
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(password, self.instance)
        return password

    class Meta:
        model = User
        fields = ['email', 'username', 'password']


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
