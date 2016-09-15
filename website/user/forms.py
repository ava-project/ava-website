from django import forms
from django.contrib.auth.models import User

from .validators import UsernameValidator

class RegisterForm(forms.ModelForm):
    email = forms.CharField(max_length=75, required=True)
    username = forms.CharField(
        max_length=75,
        validators=[UsernameValidator()],
        required=True
    )
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'A user with that email address already exists.')
        return email
