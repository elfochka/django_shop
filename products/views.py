from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin

from products.models import Category, Offer, Product

from .forms import ProductFilterForm


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


class CatalogView(BaseMixin, ListView):
    paginate_by = 6
    model = Product
    template_name = "products/catalog.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = (
            Product.objects.filter(is_deleted=False)
            .select_related("category")
            .prefetch_related("tags", "images")
        )

        form = ProductFilterForm(self.request.GET)

        if form.is_valid():
            in_stock = form.cleaned_data.get("in_stock")
            free_shipping = form.cleaned_data.get("free_shipping")
            product_name = form.cleaned_data.get("product_name")
            price_range = self.request.GET.get("price")

            if in_stock:
                queryset = queryset.annotate(total_quantity=Sum("positions__quantity"))
                queryset = queryset.filter(total_quantity__gt=0)

            if free_shipping:
                queryset = queryset.filter(free_shipping=True)
            if product_name:
                queryset = queryset.filter(title__icontains=product_name)
            if price_range:
                min_price, max_price = map(int, price_range.split(";"))
                queryset = queryset.filter(positions__price__gte=min_price, positions__price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        price_range = self.request.GET.get("price")
        if price_range:
            min_price, max_price = map(int, price_range.split(";"))
        else:
            min_price = 7
            max_price = 27
        context["min_price"] = min_price
        context["max_price"] = max_price
        context["filter_form"] = ProductFilterForm(self.request.GET)
        return context

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
