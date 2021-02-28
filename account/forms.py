from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    Meta = UserCreationForm.Meta
    Meta.fields = ('username', 'email')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
