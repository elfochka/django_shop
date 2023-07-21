from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class CatalogView(TemplateView):
    template_name = 'products/catalog.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class ProductDetailsView(TemplateView):
    template_name = 'products/product.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class CompareView(TemplateView):
    template_name = 'products/compare.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context
