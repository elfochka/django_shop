from django.views.generic import TemplateView, FormView
from django.urls import reverse
from django.conf import settings

from products.views import BaseMixin
from .forms import CheckoutStep1, CheckoutStep2, CheckoutStep3, CheckoutStep4
from .models import Deliver


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
        "4": CheckoutStep4,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = None
        self.order_id = None

    def get_context_data(self, **kwargs):
        """Put step number and sessiond data into context."""
        context = super().get_context_data(**kwargs)
        context["step"] = self.request.GET.get("step", "1")
        context["order"] = self.request.session.get(
            settings.ORDER_SESSION_ID, default={}
        )

        # Put delivery instance into context
        if context["order"]["delivery"]:
            delivery_instance = Deliver.objects.get(pk=context["order"]["delivery"])
            context["order"]["delivery"] = delivery_instance
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
            step = self.request.GET.get("step", "1")
            if step in self.form_classes.keys():
                return self.form_classes[step](initial=initial_values)

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

        if step == "4":
            # Final step - create Order, OrderItem model instances
            print("Step 4:", order)
            # ...
            self.order_id = "123456"

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        """
        Redirect user to the next step and to the payment view after the last step.
        """
        if self.step == "4":
            return "{url}?order_id={order_id}".format(
                url=reverse("orders:payment"),
                order_id=self.order_id,
            )

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
