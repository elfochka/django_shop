from django.views.generic import TemplateView


class ActionListView(TemplateView):
    template_name = "core/viewhistory.html"
