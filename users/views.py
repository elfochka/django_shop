from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from users.forms import CustomUserChangeForm
from users.models import CustomUser


class AccountDetailView(LoginRequiredMixin, TemplateView):
    template_name = "users/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context


class EmailView(TemplateView):
    template_name = "users/e-mail.html"


class PasswordView(TemplateView):
    template_name = "users/password.html"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "users/profile.html"
    success_url = reverse_lazy('users:account')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        full_name = form.cleaned_data.get("full_name")
        if full_name:
            first_name, middle_name, last_name = full_name.split(" ", 2)
            self.object.first_name = first_name
            self.object.middle_name = middle_name
            self.object.last_name = last_name
        return super().form_valid(form)


class ActionListView(TemplateView):
    template_name = "users/viewhistory.html"
