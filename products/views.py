from datetime import datetime

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin

from products.forms import ProductFilterForm, ReviewCreationForm
from products.models import AdBanner, Category, Offer, Product, Review
from users.models import Action
from users.utils import create_action


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
        """
        Put current "Limited offer" chosen product and Ad banner into context.
        """
        context = super().get_context_data(**kwargs)
        context_data = {
            "chosen_product": Product.objects.filter(is_chosen=True).first(),
            "featured_categories": Category.get_featured_categories(),
            "popular_products": Product.get_popular_products(),
            "limited_edition_products": Product.get_limited_edition_products(),
            "banners": AdBanner.get_banners()
        }
        context.update(context_data)
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

    def get_queryset(self):
        queryset = (
            Product.objects.filter(is_deleted=False)
            .select_related("category")
            .prefetch_related("tags", "images")
        )

        form = ProductFilterForm(self.request.GET)

        if form.is_valid():
            product_name = form.cleaned_data.get("product_name")
            # !Ждём реализации модели ProductPosition и нужно раскомментить, что бы фильтр полностью работал.
            # in_stock = form.cleaned_data.get("in_stock")
            # free_shipping = form.cleaned_data.get("free_shipping")
            # price_range = self.request.GET.get("price")

            if product_name:
                queryset = queryset.filter(title__icontains=product_name)

            # !Ждём реализации модели ProductPosition и нужно раскомментить, что бы фильтр полностью работал.
            # if in_stock:
            #     queryset = queryset.annotate(total_quantity=Sum("positions__quantity"))
            #     queryset = queryset.filter(total_quantity__gt=0)

            # if free_shipping:
            #     queryset = queryset.filter(free_shipping=True)

            # if price_range:
            #     min_price, max_price = map(int, price_range.split(";"))
            #     queryset = queryset.filter(positions__price__gte=min_price, positions__price__lte=max_price)

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

    def get_success_url(self):
        return reverse_lazy("products:product", args=(self.kwargs["pk"],))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewCreationForm()
        context["reviews"] = Review.objects.filter(product=self.object)
        return context

    def get(self, request, *args, **kwargs):
        """
        Create Action instance for authenticated user to track product viewing history.
        """

        if self.request.user.is_authenticated:
            create_action(
                user=self.request.user,
                verb=Action.VIEW_PRODUCT,
                target=self.get_object(),
            )

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        self.object = self.get_object()
        form = ReviewCreationForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product = self.object
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


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
