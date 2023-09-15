import re

from django import forms
from django.contrib.auth import authenticate

from users.models import CustomUser

from .models import Deliver, Order


class CheckoutStep1(forms.Form):
    name = forms.CharField(label="ФИО")
    phone = forms.CharField(label="Телефон")
    email = forms.EmailField(label="E-mail")
    password1 = forms.CharField(
        label="Пароль", required=False, widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label="Повторите пароль", required=False, widget=forms.PasswordInput()
    )

    name.widget.attrs.update({"class": "form-input", "placeholder": "Ф.И.О."})
    phone.widget.attrs.update({"class": "form-input", "placeholder": "Номер телефона"})
    email.widget.attrs.update(
        {"class": "form-input", "placeholder": "username@domain.ru"}
    )
    password1.widget.attrs.update(
        {
            "class": "form-input",
            "placeholder": "Ваш пароль – для входа или регистрации",
        }
    )
    password2.widget.attrs.update(
        {
            "class": "form-input",
            "placeholder": "Повторите пароль – только для регистрации!",
        }
    )

    def clean_phone(self):
        phone_number = self.cleaned_data.get("phone")
        if phone_number:
            if not re.match(r"^(?:\+7|8)[0-9]{10}$", phone_number):
                raise forms.ValidationError("Неверный формат номера телефона")
        return phone_number

    def clean_email(self):
        email = self.data.get("email")
        password2 = self.data.get("password2")

        # Do not allow existing emails if user is trying to signup.
        if password2 and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует!")

        return email

    def clean_password1(self):
        """Check if the user with email and password1 actually exists in database."""
        email = self.cleaned_data.get("email")
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")

        if password2 and password2 != password1:
            raise forms.ValidationError("Введённые пароли должны совпадать!")

        if (
            password1
            and not password2
            and not authenticate(None, email=email, password=password1)
        ):
            raise forms.ValidationError("Пароль неверный.")

        return password1

    def clean_password2(self):
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")
        if password2 and password2 != password1:
            raise forms.ValidationError("Введённые пароли должны совпадать!")
        return password2


class CheckoutStep2(forms.Form):
    delivery = None
    city = forms.CharField(label="Город")
    address = forms.CharField(
        label="Адрес",
        widget=forms.Textarea(
            attrs={"rows": 3, "class": "form-input", "placeholder": "Адрес доставки"}
        ),
    )

    city.widget.attrs.update({"class": "form-input", "placeholder": "Город доставки"})

    def __init__(self, *args, **kwargs):
        """Put all delivery options from the database into form field choices."""
        super().__init__(*args, **kwargs)
        deliveries = Deliver.objects.all()
        self.fields["delivery"] = forms.ChoiceField(
            label="Доставка",
            widget=forms.RadioSelect,
            choices=[(delivery.pk, delivery.title) for delivery in deliveries],
        )


class CheckoutStep3(forms.Form):
    payment = forms.ChoiceField(
        label="Способ оплаты",
        widget=forms.RadioSelect,
        choices=Order.PAYMENT_CHOICES,
    )


class CheckoutStep4(forms.Form):
    comment = forms.CharField(
        label="Комментарий к заказу",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-input",
                "placeholder": "Ваш комментарий к заказу",
            }
        ),
    )


class CardNumberForm(forms.Form):
    card_number = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "Payment-bill",
                                                                               "placeholder": "9999 9999",
                                                                               "data-mask": "9999 9999"}))
