from django.views.generic import TemplateView


class ActionListView(TemplateView):
    template_name = 'core/viewhistory.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context
