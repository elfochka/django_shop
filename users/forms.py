import re

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    full_name = forms.CharField(
        max_length=255, label="ФИО",
        widget=forms.TextInput(attrs={"placeholder": "Введите полное имя"})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "Profile-file form-input"})
    )
    email = forms.EmailField(
        max_length=255, required=False, label="Адрес эл. почты",
        widget=forms.EmailInput(attrs={"placeholder": "Введите адрес эл. почты"})
    )
    phone = forms.CharField(
        label="Введите номер телефона",
        widget=forms.TextInput(attrs={"placeholder": "89881234567"})
    )

    class Meta:
        model = CustomUser
        fields = ("image", "email", "phone")

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if full_name:
            try:
                first_name, middle_name, last_name = full_name.split(" ", 2)
                self.instance.first_name = first_name
                self.instance.middle_name = middle_name
                self.instance.last_name = last_name
            except ValueError:
                raise forms.ValidationError("Неверный формат ФИО")
        return full_name

    def clean_phone(self):
        phone_number = self.cleaned_data.get("phone")
        if phone_number:
            if not re.match(r"^(?:\+7|8)[0-9]{10}$", phone_number):
                raise forms.ValidationError("Неверный формат номера телефона")
        return phone_number

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image.name == "../static/assets/img/icons/loon-icon.svg":
            return image
        if image:
            if hasattr(image, "size"):
                if image.size > 2 * 1024 * 1024:
                    raise forms.ValidationError("Файл слишком большой. Максимальный размер - 2 МБ.")
        return image


class CustomUserChangeFormAdmin(UserChangeForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "Profile-file form-input"})
    )
    email = forms.EmailField(
        max_length=255, required=False, label="Адрес эл. почты",
        widget=forms.EmailInput(attrs={"placeholder": "Введите адрес эл. почты"})
    )
    phone = forms.CharField(
        required=False,
        label="Введите номер телефона",
        widget=forms.TextInput(attrs={"placeholder": "89881234567"})
    )

    class Meta:
        model = CustomUser
        fields = ("image", "email", "phone")

    def clean_phone(self):
        phone_number = self.cleaned_data.get("phone")
        if phone_number:
            if not re.match(r"^(?:\+7|8)[0-9]{10}$", phone_number):
                raise forms.ValidationError("Неверный формат номера телефона")
        return phone_number

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image.name == "../static/assets/img/icons/loon-icon.svg":
            return image
        if image:
            if hasattr(image, "size"):
                if image.size > 2 * 1024 * 1024:
                    raise forms.ValidationError("Файл слишком большой. Максимальный размер - 2 МБ.")
        return image
