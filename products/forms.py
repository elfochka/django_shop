from django import forms


class ProductFilterForm(forms.Form):
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)

    in_stock = forms.BooleanField(
        required=False,
        label="Только товары в наличии",
        widget=forms.CheckboxInput(attrs={})
    )

    free_shipping = forms.BooleanField(
        required=False,
        label="С бесплатной доставкой",
        widget=forms.CheckboxInput(attrs={})
    )

    product_name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"class": "form-input form-input_full", "placeholder": "Название"})
    )
