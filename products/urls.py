from django.urls import path

from products.views import (CatalogView, CompareView, ProductDetailsView,
                            SaleView)

app_name = "products"
urlpatterns = [
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("product/<int:pk>/", ProductDetailsView.as_view(), name="product"),
    path("compare/", CompareView.as_view(), name="compare"),
    path("sale/", SaleView.as_view(), name="sale"),
]
