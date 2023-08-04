from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from users.forms import CustomUserChangeForm
from users.models import CustomUser


class AccountDetailView(TemplateView):
    template_name = "users/account.html"


class EmailView(TemplateView):
    template_name = "users/e-mail.html"


class PasswordView(TemplateView):
    template_name = "users/password.html"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "users/profile.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('users:profile')


class ActionListView(TemplateView):
    template_name = "users/viewhistory.html"
