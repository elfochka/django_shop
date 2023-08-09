from datetime import datetime

from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from products.models import Category, Offer, Product, Review
from products.forms import ReviewCreationForm
from django.urls import reverse_lazy


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


class ProductDetailsView(BaseMixin, FormView, DetailView):
    template_name = "products/product.html"
    form_class = ReviewCreationForm
    queryset = (
        Product.objects.filter(is_deleted=False)
        .select_related("category")
        .prefetch_related("tags", "images")
    )
    context_object_name = "product"

    def get_success_url(self):
        return reverse_lazy('products:product', args=(self.kwargs['pk'],))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewCreationForm()
        context['reviews'] = Review.objects.filter(product_id=self.kwargs['pk']).all()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        form.instance.product_id = self.kwargs['pk']
        form.save()
        return super().form_valid(form)


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
