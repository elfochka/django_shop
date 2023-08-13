from datetime import datetime

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin

from products.forms import ReviewCreationForm
from products.models import AdBanner, Category, Offer, Product, Review


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
        chosen_product = Product.objects.filter(is_chosen=True).first()
        context["chosen_product"] = chosen_product
        context["banners"] = AdBanner.objects.filter(is_chosen=True)
        return context


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

    def get_success_url(self):
        return reverse_lazy("products:product", args=(self.kwargs["pk"],))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewCreationForm()
        context["reviews"] = Review.objects.filter(product=self.object)
        return context

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
