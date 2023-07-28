from django.views.generic import TemplateView, ListView
from django.views.generic.base import ContextMixin

from .models import Category, Product


class BaseMixin(ContextMixin):
    """
    Put data necessary for base.html template into context.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(
            parent=None, is_deleted=False
        ).order_by("pk")
        return context


class IndexView(BaseMixin, TemplateView):
    template_name = "index.html"


class CatalogView(BaseMixin, ListView):
    model = Product
    template_name = "products/catalog.html"
    queryset = (
        Product.objects.filter(is_deleted=False)
        .select_related("category")
        .prefetch_related("tags", "images")
    )
    context_object_name = "products"


class ProductDetailsView(BaseMixin, TemplateView):
    template_name = "products/product.html"


class CompareView(BaseMixin, TemplateView):
    template_name = "products/compare.html"


class SaleView(BaseMixin, TemplateView):
    template_name = "products/sale.html"
