from django.views.generic import TemplateView, FormView
from django.urls import reverse
from django.conf import settings

from products.views import BaseMixin
from .forms import CheckoutStep1, CheckoutStep2, CheckoutStep3


class CartView(TemplateView):
    template_name = "orders/cart.html"


class CheckoutView(BaseMixin, FormView):
    template_name = "orders/checkout.html"
    form_class = CheckoutStep1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = None

    def get_context_data(self, **kwargs):
        """Put step number and sessiond data into context."""
        context = super().get_context_data(**kwargs)
        context["step"] = self.request.GET.get("step", "1")
        context["order"] = self.request.session.get(
            settings.ORDER_SESSION_ID, default={}
        )
        return context

    def get_form(self, form_class=None):
        if self.request.method == "GET":
            # TODO: set form defaults for all steps using session data
            if self.request.GET.get("step") == "1":
                return CheckoutStep1(
                    initial={
                        "name": self.request.user.get_full_name(),
                        "phone": self.request.user.phone,
                        "email": self.request.user.email,
                    }
                )

            if self.request.GET.get("step") == "2":
                return CheckoutStep2(
                    initial={
                        "delivery": "ordinary",
                    }
                )

            if self.request.GET.get("step") == "3":
                return CheckoutStep3(
                    initial={
                        "payment": "online",
                    }
                )

        return super().get_form(form_class)

    def get(self, request, *args, **kwargs):
        step = self.request.GET.get("step")

        # TODO: refactor using dictionary
        if step == "1":
            self.form_class = CheckoutStep1

        if step == "2":
            self.form_class = CheckoutStep2

        if step == "3":
            self.form_class = CheckoutStep3

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        step = self.request.GET.get("step")
        # Save step value for use in `get_success_url()`
        self.step = step

        order = request.session.get(settings.ORDER_SESSION_ID, "")
        if not order:
            request.session[settings.ORDER_SESSION_ID] = {}

        if step == "1":
            self.form_class = CheckoutStep1
            form = CheckoutStep1(request.POST)
            if form.is_valid():
                order["name"] = form.cleaned_data["name"]
                order["phone"] = form.cleaned_data["phone"]
                order["email"] = form.cleaned_data["email"]

        if step == "2":
            self.form_class = CheckoutStep2
            form = CheckoutStep2(request.POST)
            if form.is_valid():
                order["delivery"] = form.cleaned_data["delivery"]
                order["city"] = form.cleaned_data["city"]
                order["address"] = form.cleaned_data["address"]

        if step == "3":
            self.form_class = CheckoutStep3
            form = CheckoutStep3(request.POST)
            if form.is_valid():
                order["payment"] = form.cleaned_data["payment"]

        request.session.modified = True
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        """
        Redirect user to the next step.
        """
        next_step = int(self.step) + 1
        return "{url}?step={step}".format(
            url=reverse("orders:checkout"),
            step=next_step,
        )


class PaymentView(TemplateView):
    template_name = "orders/payment.html"


class ProgressPaymentView(TemplateView):
    template_name = "orders/progress-payment.html"


class OrderListView(TemplateView):
    template_name = "orders/orders.html"


class OrderDetailsView(TemplateView):
    template_name = "orders/order_detail.html"
