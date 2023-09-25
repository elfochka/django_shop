from decimal import Decimal

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView

from products.cart import Cart
from products.models import ProductPosition
from products.views import BaseMixin
from users.models import CustomUser

from .forms import (CardNumberForm, CheckoutStep1, CheckoutStep2,
                    CheckoutStep3, CheckoutStep4)
from .models import Deliver, Order, OrderItem
from .tasks import check_card_number


class CartView(TemplateView):
    template_name = "orders/cart.html"


class CheckoutView(BaseMixin, FormView):
    template_name = "orders/checkout.html"
    form_class = CheckoutStep1

    STEP_1_CLIENT_INFO = "1"
    STEP_2_DELIVERY_OPTIONS = "2"
    STEP_3_PAYMENT_OPTIONS = "3"
    STEP_4_SUBMIT_ORDER = "4"

    # Form classes for each step
    form_classes = {
        STEP_1_CLIENT_INFO: CheckoutStep1,
        STEP_2_DELIVERY_OPTIONS: CheckoutStep2,
        STEP_3_PAYMENT_OPTIONS: CheckoutStep3,
        STEP_4_SUBMIT_ORDER: CheckoutStep4,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = None
        self.order_id = None

    def get_context_data(self, **kwargs):
        """Put step number and sessiond data into context."""
        context = super().get_context_data(**kwargs)
        context["step"] = self.request.GET.get("step", self.STEP_1_CLIENT_INFO)
        context["order"] = self.request.session.get(
            settings.ORDER_SESSION_ID, default={}
        )

        # Put delivery instance and delivery price into context
        if context["order"].get("delivery"):
            cart = Cart(self.request)
            delivery_instance = Deliver.objects.get(pk=context["order"]["delivery"])
            delivery_price = cart.get_delivery_price(delivery_instance)
            total_price = cart.get_total_products_price() + delivery_price
            context["order"]["delivery"] = delivery_instance
            context["order"]["delivery_price"] = delivery_price
            context["order"]["total_price"] = total_price
        return context

    def get_form(self, form_class=None):
        """Fill form for current step with initial values taken from `order` dict in the session."""
        if self.request.method == "GET":
            request_user_name = ""
            request_user_phone = ""
            request_user_email = ""

            if self.request.user.is_authenticated:
                request_user_name = self.request.user.get_full_name()
                request_user_phone = self.request.user.phone
                request_user_email = self.request.user.email

            order = self.request.session.get(settings.ORDER_SESSION_ID, {})
            initial_values = {
                "name": order.get("name", None) or request_user_name,
                "phone": order.get("phone", None) or request_user_phone,
                "email": order.get("email", None) or request_user_email,
                "delivery": order.get("delivery", "ordinary"),
                "city": order.get("city", ""),
                "address": order.get("address", ""),
                "payment": order.get("payment", "online"),
                "comment": order.get("comment", ""),
            }
            step = self.request.GET.get("step", self.STEP_1_CLIENT_INFO)
            if step in self.form_classes.keys():
                return self.form_classes[step](initial=initial_values)

        return super().get_form(form_class)

    def get(self, request, *args, **kwargs):
        """Set form for current step."""
        step = self.request.GET.get("step", self.STEP_1_CLIENT_INFO)
        if step in self.form_classes.keys():
            self.form_class = self.form_classes[step]

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Save input from the form into `order` dict in the session."""
        step = self.request.GET.get("step", self.STEP_1_CLIENT_INFO)
        # Save step value for use in `get_success_url()`
        self.step = step

        # Get order dict from session, create it if it not exists yet
        order = request.session.get(settings.ORDER_SESSION_ID, "")
        if not order:
            order = request.session[settings.ORDER_SESSION_ID] = {}

        # Use form for the current step to validate input, and store it in session
        if step in self.form_classes.keys():
            self.form_class = self.form_classes[step]
            form = self.form_classes[step](request.POST)
            if form.is_valid():
                for key in form.cleaned_data.keys():
                    order[key] = form.cleaned_data[key]

        request.session.modified = True

        # Store order and cart dicts from session in the copy
        order_copy = order.copy()
        cart_copy = self.request.session[settings.CART_SESSION_ID].copy()

        user = None

        # Handle user login (existing user with "email" and "password1")
        if (
            step == self.STEP_1_CLIENT_INFO
            and not self.request.user.is_authenticated
            and order.get("password1")
            and not order.get("password2")
        ):
            # Login user and proceed to step 2 (email & password1 pair checked in the form clean method,
            # so it should be valid here).
            user = authenticate(
                self.request,
                email=order["email"],
                password=order["password1"],
            )

        # Handle new user signup
        if (
            step == self.STEP_1_CLIENT_INFO
            and not self.request.user.is_authenticated
            and order.get("password1")
            and order.get("password2")
        ):
            # Create new user with provided info
            user = CustomUser.objects.create_user(
                username=order["email"],
                email=order["email"],
                password=order["password1"],
                phone=order["phone"],
            )

        # We created new user, or authenticated as existing one => login:
        if user:
            # Login user, session data will be lost
            login(
                self.request,
                user,
                backend="allauth.account.auth_backends.AuthenticationBackend",
            )
            # Restore order and cart in session from copies
            self.request.session[settings.CART_SESSION_ID] = cart_copy
            self.request.session[settings.ORDER_SESSION_ID] = order_copy
            request.session.modified = True
            return redirect(reverse("orders:checkout") + "?step=2")

        # Check product position availability before proceeding to the last step
        if step == self.STEP_3_PAYMENT_OPTIONS:
            cart = self.request.session[settings.CART_SESSION_ID]

            for product_position_id in cart.keys():
                product_position_instance = ProductPosition.objects.get(pk=product_position_id)
                quantity = int(cart[product_position_id]["quantity"])
                if quantity > product_position_instance.quantity:
                    cart[product_position_id]["quantity"] = product_position_instance.quantity

            self.request.session.modified = True

        # Handle order submit on the last step
        if step == self.STEP_4_SUBMIT_ORDER:
            # Final step - create Order, OrderItem model instances
            client = self.request.user if self.request.user.is_authenticated else None
            delivery = Deliver.objects.get(pk=order["delivery"])
            delivery_price = Cart(self.request).get_delivery_price(delivery=delivery)

            # Create Order instance
            order_instance = Order.objects.create(
                client=client,
                delivery=delivery,
                delivery_price=delivery_price,
                payment=order["payment"],
                status="created",
                name=order["name"],
                phone=order["phone"],
                email=order["email"],
                city=order["city"],
                address=order["address"],
                comment=order["comment"],
            )
            self.order_id = order_instance.pk

            # Create OrderItem instances
            cart = self.request.session[settings.CART_SESSION_ID]
            for product_position_id in cart.keys():
                product_position_instance = ProductPosition.objects.get(
                    pk=product_position_id
                )
                quantity = int(cart[product_position_id]["quantity"])
                price = Decimal(cart[product_position_id]["price"])
                total_price = price * quantity
                if quantity:
                    OrderItem.objects.create(
                        order=order_instance,
                        product_position=product_position_instance,
                        price=total_price,
                        quantity=quantity,
                    )

            # Reset cart
            self.request.session[settings.CART_SESSION_ID] = {}
            self.request.session.modified = True

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        """
        Redirect user to the next step and to the payment view after the last step.
        """
        if self.step == self.STEP_4_SUBMIT_ORDER:
            return "{url}?order_id={order_id}".format(
                url=reverse("orders:payment"),
                order_id=self.order_id,
            )

        next_step = int(self.step) + 1
        return "{url}?step={step}".format(
            url=reverse("orders:checkout"),
            step=next_step,
        )


class PaymentView(FormView):
    form_class = CardNumberForm

    def get_template_names(self):
        order = self.request.session.get(settings.ORDER_SESSION_ID, "")
        order["order_id"] = self.request.GET.get("order_id")
        if order["payment"] == "online":
            return ["orders/payment.html"]
        else:
            return ["orders/paymentsomeone.html"]

    def get_success_url(self):
        return reverse_lazy("orders:progress-payment")

    def post(self, request, *args, **kwargs):
        order = self.request.session.get(settings.ORDER_SESSION_ID, "")
        form = self.get_form()
        if form.is_valid():
            check_card_number.delay(self.request.POST.get("card_number", "0"), order["order_id"])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PaymentViewWithParams(FormView):
    form_class = CardNumberForm
    template_name = "orders/paymentsomeone.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_id"] = self.kwargs["order_id"]
        return context

    def get_success_url(self):
        return reverse_lazy("orders:progress-payment")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            check_card_number.delay(self.request.POST.get("card_number", "0"), self.kwargs["order_id"])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ProgressPaymentView(TemplateView):
    template_name = "orders/progress-payment.html"


class OrderListView(TemplateView):
    template_name = "orders/orders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class OrderDetailsView(TemplateView):
    template_name = "orders/order_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["order"] = Order.objects.filter(id=self.kwargs["pk"]).first()
        context["products"] = OrderItem.objects.select_related("product_position").filter(order_id=self.kwargs["pk"])
        return context
