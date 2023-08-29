from django import forms


class CheckoutStep1(forms.Form):
    name = forms.CharField(label="ФИО")
    phone = forms.CharField(label="Телефон")
    email = forms.CharField(label="E-mail")

    name.widget.attrs.update({"class": "form-input"})
    phone.widget.attrs.update({"class": "form-input"})
    email.widget.attrs.update({"class": "form-input"})


class CheckoutStep2(forms.Form):
    CHOICES = [
        ("ordinary", "Обычная доставка"),
        ("express", "Экспресс доставка"),
    ]

    delivery = forms.ChoiceField(
        label="Доставка",
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
    city = forms.CharField(label="Город")
    address = forms.CharField(
        label="Адрес",
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-input"}),
    )

    city.widget.attrs.update({"class": "form-input"})


class CheckoutStep3(forms.Form):
    CHOICES = [
        ("online", "Онлайн картой"),
        ("someone", "Онлайн со случайного чужого счета"),
    ]

    payment = forms.ChoiceField(
        label="Способ оплаты",
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
