from django.forms import ModelForm, Textarea

from products.models import Review


class ReviewCreationForm(ModelForm):
    class Meta:
        model = Review
        fields = ("body",)
        widgets = {
            "body": Textarea(attrs={"placeholder": "Отзыв", "class": "form-textarea"}),
        }
