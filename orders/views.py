from django.views.generic import TemplateView


class CartView(TemplateView):
    template_name = "orders/cart.html"


class CheckoutView(TemplateView):
    template_name = "orders/checkout.html"


class PaymentView(TemplateView):
    template_name = "orders/payment.html"


class ProgressPaymentView(TemplateView):
    template_name = "orders/progress-payment.html"


class OrderListView(TemplateView):
    template_name = "orders/orders.html"


class OrderDetailsView(TemplateView):
    template_name = "orders/order_detail.html"
