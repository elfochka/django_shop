from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
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
        """Put current "Limited offer" chosen product and Ad banner into context."""
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

            query = self.request.GET.get("query")
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | Q(title__icontains=query.capitalize())
                    | Q(title__icontains=query.lower())
                )
            category = self.request.GET.get("category")
            if category:
                queryset = queryset.filter(category=category)

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


def add_to_comparison(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comparison_products = request.session.get('comparison_products', [])
    if len(comparison_products) >= 4:
        del request.session['comparison_products']
        comparison_products = []
    if pk in comparison_products:
        comparison_products.remove(pk)
        request.session['comparison_products'] = comparison_products
    else:
        comparison_products.append(pk)
        request.session['comparison_products'] = comparison_products

    referer = request.META.get('HTTP_REFERER', None)
    if referer:
        return HttpResponseRedirect(referer)
    else:
        return redirect('products:catalog')


class CompareView(BaseMixin, TemplateView):
    template_name = "products/compare.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comparison_ids = self.request.session.get('comparison_products', [])
        products_to_compare = Product.objects.filter(id__in=comparison_ids)
        show_differences = self.request.GET.get('show_differences', 'true').lower() == 'true'

        if len(products_to_compare) < 2:
            context['error_message'] = 'Недостаточно данных для сравнения'
            return context

        all_categories_equal = all(p.category == products_to_compare[0].category for p in products_to_compare)
        common_features = {key: True for key in (products_to_compare[0].features or {}).keys()}

        for product in products_to_compare:
            product_features = product.features or {}
            for key in common_features.keys():
                if key not in product_features or product_features[key] != products_to_compare[0].features[key]:
                    common_features[key] = False

            average_price = product.productposition_set.aggregate(Avg('price'))['price__avg']

            if average_price is not None:
                offers = Offer.objects.filter(
                    is_active=True,
                    date_start__lte=datetime.today(),
                    date_end__gte=datetime.today(),
                ).filter(
                    Q(products__in=[product]) |
                    Q(categories__in=[product.category])
                )

                for offer in offers:
                    if offer.discount_type == Offer.Types.DISCOUNT_PERCENT:
                        average_price -= (average_price * offer.discount_value) / 100
                    elif offer.discount_type == Offer.Types.DISCOUNT_AMOUNT:
                        average_price -= offer.discount_value
                    elif offer.discount_type == Offer.Types.FIXED_PRICE:
                        average_price = offer.discount_value

                product.calculated_price = round(average_price, 2)

        highlighted_keys = [key for key, value in common_features.items() if value]

        common_keys = set(products_to_compare[0].features.keys()) if products_to_compare[0].features else set()

        for product in products_to_compare[1:]:
            product_keys = set(product.features.keys()) if product.features else set()
            common_keys.intersection_update(product_keys)

        has_common_features = bool(common_keys)

        if not has_common_features and not all_categories_equal:
            context[
                'impossible_to_compare'] = 'Величина мира и его явлений такова, ' \
                                           'что все попытки сравнения между несравнимыми ' \
                                           'вещами лишь уменьшают их уникальность.'
            context['products'] = products_to_compare
            return context

        context['products'] = products_to_compare
        context['all_categories_equal'] = all_categories_equal
        context['highlighted_keys'] = highlighted_keys
        context['show_differences'] = show_differences

        return context


class SaleView(BaseMixin, ListView):
    model = Offer
    template_name = "products/sale.html"
    queryset = Offer.objects.filter(
        is_active=True,
        date_start__lte=datetime.now(),
        date_end__gte=datetime.now(),
    ).prefetch_related("products", "categories")
    context_object_name = "offers"
