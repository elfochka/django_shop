from django import forms

from .models import Deliver, Order


class CheckoutStep1(forms.Form):
    name = forms.CharField(label="ФИО")
    phone = forms.CharField(label="Телефон")
    email = forms.CharField(label="E-mail")

    name.widget.attrs.update({"class": "form-input"})
    phone.widget.attrs.update({"class": "form-input"})
    email.widget.attrs.update({"class": "form-input"})


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
