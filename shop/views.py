from django.views.generic import TemplateView


class SaleView(TemplateView):
    template_name = "shop/sale.html"
