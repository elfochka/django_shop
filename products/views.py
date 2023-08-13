from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin

from products.models import AdBanner, Category, Offer, Product


class BaseMixin(ContextMixin):
    """Put data necessary for base.html template into context."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(
            parent=None, is_deleted=False
        ).order_by("pk")
        return context


class IndexView(BaseMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["banners"] = AdBanner.objects.filter(is_chosen=True)
        return context_data


class CatalogView(BaseMixin, ListView):
    paginate_by = 6
    model = Product
    template_name = "products/catalog.html"
    queryset = (
        Product.objects.filter(is_deleted=False)
        .select_related("category")
        .prefetch_related("tags", "images")
    )
    context_object_name = "products"

    def listing(self):
        catalog = Product.objects.all()
        paginator = Paginator(catalog, 6)
        page_number = self.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(self, "products/catalog.html", {"page_obj": page_obj})


class ProductDetailsView(BaseMixin, DetailView):
    template_name = "products/product.html"
    queryset = (
        Product.objects.filter(is_deleted=False)
        .select_related("category")
        .prefetch_related("tags", "images")
    )
    context_object_name = "product"


class CompareView(BaseMixin, TemplateView):
    template_name = "products/compare.html"


class SaleView(BaseMixin, ListView):
    model = Offer
    template_name = "products/sale.html"
    queryset = Offer.objects.filter(
        is_active=True,
        date_start__lte=datetime.now(),
        date_end__gte=datetime.now(),
    ).prefetch_related("products", "categories")
    context_object_name = "offers"
