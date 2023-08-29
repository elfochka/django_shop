from django import forms


class CheckoutStep1(forms.Form):
    name = forms.CharField()
    phone = forms.CharField()
    email = forms.CharField()


class CheckoutStep2(forms.Form):
    delivery = forms.CharField()
    city = forms.CharField()
    address = forms.CharField()


class CheckoutStep3(forms.Form):
    payment = forms.CharField()
