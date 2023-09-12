from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, UpdateView

from orders.models import Order
from users.forms import CustomUserChangeForm
from users.models import Action, CustomUser


class AccountDetailView(LoginRequiredMixin, TemplateView):
    template_name = "users/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["orders"] = Order.objects.filter(client_id=self.request.user)
        return context


class EmailView(TemplateView):
    template_name = "users/e-mail.html"


class PasswordView(TemplateView):
    template_name = "users/password.html"


class HistoryOrderView(TemplateView):
    template_name = "users/historyorder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["orders"] = Order.objects.filter(client_id=self.request.user)
        return context


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
    queryset = Action.objects.filter(verb=Action.VIEW_PRODUCT)
    context_object_name = "actions"

    def get_queryset(self):
        """
        Get last 20 product views for authenticated user.
        """
        return self.queryset.filter(user=self.request.user)[:20]
