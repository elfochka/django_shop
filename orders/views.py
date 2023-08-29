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
    # Form classes for each step
    form_classes = {
        "1": CheckoutStep1,
        "2": CheckoutStep2,
        "3": CheckoutStep3,
    }

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
        """Fill form for current step with initial values taken from `order` dict in the session."""
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
        """Set form for current step."""
        step = self.request.GET.get("step", "1")
        if step in self.form_classes.keys():
            self.form_class = self.form_classes[step]

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Save input from the form into `order` dict in the session."""
        step = self.request.GET.get("step", "1")
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
