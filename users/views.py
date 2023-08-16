from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView

from users.forms import CustomUserChangeForm
from users.models import CustomUser
from products.models import Action


class AccountDetailView(LoginRequiredMixin, TemplateView):
    template_name = "users/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class EmailView(TemplateView):
    template_name = "users/e-mail.html"


class PasswordView(TemplateView):
    template_name = "users/password.html"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:account")

    def get_initial(self):
        initial = super().get_initial()
        initial["full_name"] = self.request.user.get_full_name()
        return initial


class ActionListView(LoginRequiredMixin, ListView):
    model = Action
    template_name = "users/viewhistory.html"
    queryset = Action.objects.all()
    context_object_name = "actions"

    def get_queryset(self):
        """
        Get last 20 product views for authenticated user.
        """
        queryset = Action.objects.filter(
            user=self.request.user,
            verb=Action.Verb.VIEW_PRODUCT,
        )[:20]
        return queryset
