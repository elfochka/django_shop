from django.views.generic import TemplateView


class CartView(TemplateView):
    template_name = 'orders/cart.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class CheckoutView(TemplateView):
    template_name = 'orders/checkout.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class PaymentView(TemplateView):
    template_name = 'orders/payment.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class ProgressPaymentView(TemplateView):
    template_name = 'orders/progress-payment.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class OrderListView(TemplateView):
    template_name = 'orders/orders.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class OrderDetailsView(TemplateView):
    template_name = 'orders/order_detail.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context
