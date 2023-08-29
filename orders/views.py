from django.views import View
from django.views.generic import TemplateView, FormView
from django.urls import reverse

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
        """Put step number into context."""
        context = super().get_context_data(**kwargs)
        context["step"] = self.request.GET.get("step", "1")
        return context

    def get(self, request, *args, **kwargs):
        step = self.request.GET.get("step")

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

        if step == "1":
            self.form_class = CheckoutStep1
            form = CheckoutStep1(request.POST)
            if form.is_valid():
                print("Name.:", form.cleaned_data["name"])
                print("Phone:", form.cleaned_data["phone"])
                print("Email:", form.cleaned_data["email"])
                # TODO: Save name and phone into session

        if step == "2":
            self.form_class = CheckoutStep2
            form = CheckoutStep2(request.POST)
            if form.is_valid():
                print("Delivery.:", form.cleaned_data["delivery"])
                print("City.....:", form.cleaned_data["city"])
                print("Address..:", form.cleaned_data["address"])
                # TODO: Save stuff into session
                # TODO: Handle form errors

        if step == "3":
            self.form_class = CheckoutStep3
            form = CheckoutStep3(request.POST)
            if form.is_valid():
                print("Payment:", form.cleaned_data["payment"])

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
