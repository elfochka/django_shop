import re

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        initial = kwargs.get('initial', {})
        initial['full_name'] = self.request.user.get_full_name()
        kwargs['initial'] = initial
        return kwargs

    def form_valid(self, form):
        full_name = form.cleaned_data.get("full_name")
        phone_number = form.cleaned_data.get("phone")

        if phone_number:
            if not re.match(r"^(?:\+7|8)[0-9]{10}$", phone_number):
                form.add_error("phone", "Неверный формат номера телефона")
                return self.form_invalid(form)
        if full_name:
            try:
                first_name, middle_name, last_name = full_name.split(" ", 2)
                form.instance.first_name = first_name
                form.instance.middle_name = middle_name
                form.instance.last_name = last_name
            except ValueError:
                form.add_error("full_name", "Неверный формат ФИО")
                return self.form_invalid(form)
        return super().form_valid(form)


class ActionListView(TemplateView):
    template_name = "users/viewhistory.html"
