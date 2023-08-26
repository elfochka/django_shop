from django.urls import path

from products.views import (CatalogView, CompareView, ProductDetailsView,
                            SaleView, add_to_comparison)

app_name = "products"
urlpatterns = [
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("catalog//<int:page>", CatalogView.listing, name="catalog-by-page"),
    path("product/<int:pk>/", ProductDetailsView.as_view(), name="product"),
    path("compare/", CompareView.as_view(), name="compare"),
    path('add_to_comparison/<int:pk>/', add_to_comparison, name='add_to_comparison'),
    path("sale/", SaleView.as_view(), name="sale"),
]
