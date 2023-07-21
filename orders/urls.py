from django.urls import path

from orders.views import (
    CartView,
    CheckoutView,
    PaymentView,
    ProgressPaymentView,
    OrderListView,
    OrderDetailsView,
)

app_name = 'orders'
urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('progress-payment/', ProgressPaymentView.as_view(), name='progress-payment'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailsView.as_view(), name='order_detail'),
]
