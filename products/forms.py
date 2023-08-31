from django import forms
from django.forms import ModelForm, Textarea

from products.models import Review


class ReviewCreationForm(ModelForm):
    class Meta:
        model = Review
        fields = ("body",)
        widgets = {
            "body": Textarea(attrs={"placeholder": "Отзыв", "class": "form-textarea"}),
        }


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


class AddProductToCartForm(forms.Form):
    """
    Form to add products to the cart or override quantity of product_position already  in the cart.
    """

    quantity = forms.IntegerField()
    is_override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
