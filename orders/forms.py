import re

from django import forms

from .models import Deliver, Order


class CheckoutStep1(forms.Form):
    name = forms.CharField(label="ФИО")
    phone = forms.CharField(label="Телефон")
    email = forms.EmailField(label="E-mail")

    name.widget.attrs.update({"class": "form-input"})
    phone.widget.attrs.update({"class": "form-input"})
    email.widget.attrs.update({"class": "form-input"})

    def clean_phone(self):
        phone_number = self.cleaned_data.get("phone")
        if phone_number:
            if not re.match(r"^(?:\+7|8)[0-9]{10}$", phone_number):
                raise forms.ValidationError("Неверный формат номера телефона")
        return phone_number


class CheckoutStep2(forms.Form):
    delivery = None
    city = forms.CharField(label="Город")
    address = forms.CharField(
        label="Адрес",
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-input"}),
    )

    city.widget.attrs.update({"class": "form-input"})

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
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-input"}),
    )
