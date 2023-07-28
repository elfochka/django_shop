from django.views.generic import TemplateView

from .models import Category


class BaseView(TemplateView):
    """
    Put data necessary for base.html template into context.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(
            parent=None, is_deleted=False
        ).order_by("pk")
        return context


class IndexView(BaseView):
    template_name = "index.html"


class CatalogView(BaseView):
    template_name = "products/catalog.html"


class ProductDetailsView(BaseView):
    template_name = "products/product.html"


class CompareView(BaseView):
    template_name = "products/compare.html"


class SaleView(BaseView):
    template_name = "products/sale.html"
