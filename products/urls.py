from django.urls import path

from products.views import (
    CatalogView,
    CompareView,
    ProductDetailsView,
    SaleView,
    cart_detail,
    cart_add,
    cart_remove,
)

app_name = "products"
urlpatterns = [
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("catalog//<int:page>", CatalogView.listing, name="catalog-by-page"),
    path("product/<int:pk>/", ProductDetailsView.as_view(), name="product"),
    path("compare/", CompareView.as_view(), name="compare"),
    path("sale/", SaleView.as_view(), name="sale"),
    path("cart/", cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", cart_remove, name="cart_remove"),
]
