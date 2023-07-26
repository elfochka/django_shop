from django.views.generic import TemplateView


class AccountDetailView(TemplateView):
    template_name = 'users/account.html'


class RegisterView(TemplateView):
    template_name = "users/registration.html"


class LoginView(TemplateView):
    template_name = "users/login.html"


class EmailView(TemplateView):
    template_name = "users/e-mail.html"


class PasswordView(TemplateView):
    template_name = "users/password.html"


class ProfileView(TemplateView):
    template_name = "users/profile.html"


class UserProfileUpdateForm(TemplateView):
    template_name = "users/profile_update.html"