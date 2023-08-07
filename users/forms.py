from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    full_name = forms.CharField(max_length=255, label="ФИО")

    class Meta:
        model = CustomUser
        fields = ("image", "email", "phone", "first_name", "middle_name", "last_name")
