from django.views.generic import TemplateView


class AccountDetailView(TemplateView):
    template_name = 'users/account.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class RegisterView(TemplateView):
    template_name = 'users/registration.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class LoginView(TemplateView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class EmailView(TemplateView):
    template_name = 'users/e-mail.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class PasswordView(TemplateView):
    template_name = 'users/password.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class ProfileView(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context


class UserProfileUpdateForm(TemplateView):
    template_name = 'users/profile_update.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context
