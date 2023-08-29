from django.views.generic import TemplateView

from products.views import BaseMixin


class CartView(TemplateView):
    template_name = "orders/cart.html"


class CheckoutView(BaseMixin, TemplateView):
    template_name = "orders/checkout.html"

    def get_context_data(self, **kwargs):
        """Put step number into context."""
        context = super().get_context_data(**kwargs)
        context["step"] = self.request.GET.get("step", "1")
        return context


class PaymentView(TemplateView):
    template_name = "orders/payment.html"


class ProgressPaymentView(TemplateView):
    template_name = "orders/progress-payment.html"


class OrderListView(TemplateView):
    template_name = "orders/orders.html"


class OrderDetailsView(TemplateView):
    template_name = "orders/order_detail.html"
