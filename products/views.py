from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class CatalogView(TemplateView):
    template_name = "products/catalog.html"


class ProductDetailsView(TemplateView):
    template_name = "products/product.html"


class CompareView(TemplateView):
    template_name = "products/compare.html"
