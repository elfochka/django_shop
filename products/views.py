from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Min, Q, Sum
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin

from products.cart import Cart
from products.forms import (AddProductToCartForm, ProductFilterForm,
                            ReviewCreationForm)
from products.models import (AdBanner, Category, Offer, Product,
                             ProductPosition, Review)
from users.models import Action
from users.utils import create_action


class BaseMixin(ContextMixin):
    """Put data necessary for base.html template into context."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = (
            Category.objects.filter(parent=None, is_deleted=False)
            .order_by("pk")
            .prefetch_related("subcategories")
        )
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
            "banners": AdBanner.get_banners(),
            "categories": Category.objects.filter(parent=None, is_deleted=False)
            .order_by("pk")
            .prefetch_related("subcategories")
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
            in_stock = form.cleaned_data.get("in_stock")
            free_shipping = form.cleaned_data.get("free_shipping")
            price_range = self.request.GET.get("price")
            sort_param = self.request.GET.get("sort_param")
            tag_chosen = self.request.GET.get("tags")

            if product_name:
                queryset = queryset.filter(
                    Q(title__icontains=product_name)
                    | Q(title__icontains=product_name.capitalize())
                    | Q(title__icontains=product_name.lower())
                )

            query = self.request.GET.get("query")
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query)
                    | Q(title__icontains=query.capitalize())
                    | Q(title__icontains=query.lower())
                )
            category = self.request.GET.get("category")
            if category:
                queryset = queryset.filter(category=category)

            if in_stock:
                queryset = queryset.annotate(total_quantity=Sum("productposition__quantity"))
                queryset = queryset.filter(total_quantity__gt=0)

            if free_shipping:
                queryset = queryset.filter(productposition__free_shipping=True)

            if price_range or sort_param == "price_l2h" or sort_param == "price_h2l":
                queryset = queryset.annotate(price=Avg("productposition__price"))

            if price_range:
                min_price, max_price = map(int, price_range.split(";"))
                queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

            if sort_param == "price_l2h":
                queryset = queryset.order_by("price")

            elif sort_param == "price_h2l":
                queryset = queryset.order_by("-price")

            if sort_param == "pop_l2h":
                queryset = queryset.annotate(count_orders=Count("productposition__orderitem__order"))
                queryset = queryset.order_by("count_orders")
            elif sort_param == "pop_h2l":
                queryset = queryset.annotate(count_orders=Count("productposition__orderitem__order"))
                queryset = queryset.order_by("-count_orders")

            if sort_param == "review_l2h":
                queryset = queryset.annotate(count_reviews=Count("reviews"))
                queryset = queryset.order_by("count_reviews")
            elif sort_param == "review_h2l":
                queryset = queryset.annotate(count_reviews=Count("reviews"))
                queryset = queryset.order_by("-count_reviews")

            if sort_param == "new_l2h":
                queryset = queryset.order_by("updated")
            elif sort_param == "new_h2l":
                queryset = queryset.order_by("-updated")

            if tag_chosen:
                queryset = queryset.filter(tags=tag_chosen)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        price_range = self.request.GET.get("price")
        min_price_of_all = ProductPosition.objects.values("price").aggregate(Min("price"))["price__min"]
        max_price_of_all = ProductPosition.objects.values("price").aggregate(Max("price"))["price__max"]
        sort_param = self.request.GET.get("sort_param")
        if price_range:
            min_price, max_price = map(int, price_range.split(";"))
        else:
            min_price = min_price_of_all
            max_price = max_price_of_all
        context["min_price"] = min_price
        context["max_price"] = max_price
        context["min_price_of_all"] = min_price_of_all
        context["max_price_of_all"] = max_price_of_all
        context["sort_param"] = sort_param
        context["filter_form"] = ProductFilterForm(self.request.GET)

        payload = ""
        for k, list_ in self.request.GET.lists():
            if k == "page":
                continue
            for v in list_:
                payload += "&" + k + "=" + v
        context["payload"] = payload

        payload = ""
        for k, list_ in self.request.GET.lists():
            if k == "page" or k == "sort_param":
                continue
            for v in list_:
                payload += "&" + k + "=" + v
        context["sort_payload"] = payload

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
        context[
            "product_positions"
        ] = self.object.productposition_set.all().prefetch_related("seller")
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
    comparison_products = request.session.get("comparison_products", [])
    if len(comparison_products) >= 4:
        del request.session["comparison_products"]
        comparison_products = []
    if pk in comparison_products:
        comparison_products.remove(pk)
        request.session["comparison_products"] = comparison_products
    else:
        comparison_products.append(pk)
        request.session["comparison_products"] = comparison_products

    referer = request.META.get("HTTP_REFERER", None)
    if referer:
        return HttpResponseRedirect(referer)
    else:
        return redirect("products:catalog")


class CompareView(BaseMixin, TemplateView):
    template_name = "products/compare.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comparison_ids = self.request.session.get("comparison_products", [])
        products_to_compare = Product.objects.filter(id__in=comparison_ids)

        show_differences = (
            self.request.GET.get("show_differences", "true").lower() == "true"
        )

        if len(products_to_compare) < 2:
            context["error_message"] = "Недостаточно данных для сравнения"
            return context

        all_categories_equal = all(
            p.category == products_to_compare[0].category for p in products_to_compare
        )
        common_features = {
            key: True for key in (products_to_compare[0].features or {}).keys()
        }

        for product in products_to_compare:
            product_features = product.features or {}
            for key in common_features.keys():
                if (
                    key not in product_features
                    or product_features[key] != products_to_compare[0].features[key]
                ):
                    common_features[key] = False

        highlighted_keys = [key for key, value in common_features.items() if value]

        common_keys = (
            set(products_to_compare[0].features.keys())
            if products_to_compare[0].features
            else set()
        )

        for product in products_to_compare[1:]:
            product_keys = set(product.features.keys()) if product.features else set()
            common_keys.intersection_update(product_keys)

        has_common_features = bool(common_keys)

        if not has_common_features and not all_categories_equal:
            context["impossible_to_compare"] = (
                "Величина мира и его явлений такова, "
                "что все попытки сравнения между несравнимыми "
                "вещами лишь уменьшают их уникальность."
            )
            context["products"] = products_to_compare
            return context

        context["products"] = products_to_compare
        context["all_categories_equal"] = all_categories_equal
        context["highlighted_keys"] = highlighted_keys
        context["show_differences"] = show_differences

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


@require_POST
def cart_add_product(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    View for adding the product with the cheapest position to the cart.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to add to the cart.

    Returns:
        HttpResponse: Redirects to the product page or cart detail page.

    Note:
        If no product position is available for the selected product, it redirects
        the user back to the product page. If successful, it adds the product to the cart
        with the quantity specified in the form, or the maximum available quantity if specified
        quantity exceeds the stock.

    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cheapest_position = product.get_lowest_price_position

    if not cheapest_position:
        return redirect(reverse_lazy("products:product", kwargs={"pk": product_id}))

    form = AddProductToCartForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        quantity = (
            data["quantity"]
            if int(data["quantity"]) <= cheapest_position.quantity
            else cheapest_position.quantity
        )
        cart.add(
            product_position=cheapest_position,
            quantity=quantity,
            override_quantity=data["is_override"],
        )

        if data["is_override"]:
            return redirect("products:cart_detail")

    return redirect(
        reverse_lazy("products:product", kwargs={"pk": product_id}) + "#modal_open"
    )


@require_POST
def cart_add_product_position(
    request: HttpRequest, product_position_id: int
) -> HttpResponse:
    """
    View for adding specified product position of the product to the cart
    or updating quantities for already added product positions.
    """
    cart = Cart(request)
    product_position = ProductPosition.objects.get(pk=product_position_id)
    # If there's no such product position, redirect user to the product catalogue
    if not product_position:
        return redirect(reverse_lazy("products:catalog"))

    form = AddProductToCartForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        # Add only available quantity
        quantity = (
            data["quantity"]
            if int(data["quantity"]) <= product_position.quantity
            else product_position.quantity
        )
        cart.add(
            product_position=product_position,
            quantity=quantity,
            override_quantity=data["is_override"],
        )
        # We  only set `is_override` to True in cart detailed view, so redirect user there
        if data["is_override"]:
            return redirect("products:cart_detail")
    # No form data - we are adding from product page, sellers tab:
    else:
        cart.add(
            product_position=product_position,
            quantity=1,
            override_quantity=False,
        )

    # Redirect to product page, and open the modal
    return redirect(
        reverse_lazy("products:product", kwargs={"pk": product_position.product.id})
        + "#modal_open"
    )


@require_POST
def cart_remove(request: HttpRequest, product_position_id) -> HttpResponse:
    """
    View to remove product positions from the cart.
    """
    cart = Cart(request)
    product_position = get_object_or_404(ProductPosition, id=product_position_id)
    cart.remove(product_position=product_position)

    return redirect("products:cart_detail")


class CartDetailView(BaseMixin, TemplateView):
    template_name = "orders/cart.html"
