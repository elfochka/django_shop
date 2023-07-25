from django.urls import path

from shop.views import (
    SaleView,
)

app_name = "shop"
urlpatterns = [
    path('sale/', SaleView.as_view(), name="sale"),
]
