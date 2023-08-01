from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from users.forms import UserLoginForm, UserRegistrationForm


class AccountDetailView(TemplateView):
    template_name = "users/account.html"


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:account")
    template_name = "users/registration.html"


class EmailView(TemplateView):
    template_name = "users/e-mail.html"


class PasswordView(TemplateView):
    template_name = "users/password.html"


class ProfileView(TemplateView):
    template_name = "users/profile.html"


class UserProfileUpdateForm(TemplateView):
    template_name = "users/profile_update.html"


class ActionListView(TemplateView):
    template_name = "users/viewhistory.html"
