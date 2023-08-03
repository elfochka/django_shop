from django.views.generic import TemplateView


class AccountDetailView(TemplateView):
    template_name = "users/account.html"


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
