from django.views.generic import TemplateView


class SaleView(TemplateView):
    template_name = 'shop/sale.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context



