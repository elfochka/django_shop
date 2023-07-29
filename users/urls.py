from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import (
    AccountDetailView,
    RegisterView,
    # register,
    # LoginView,
    EmailView,
    PasswordView,
    ProfileView,
    UserProfileUpdateForm,
    ActionListView,
)

app_name = "users"

urlpatterns = [
    path("account/", AccountDetailView.as_view(), name="account"),
    path('registration/', RegisterView.as_view(), name="registration"),
    path("login/", LoginView.as_view(template_name='../templates/users/login.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("e-mail/", EmailView.as_view(), name="e-mail"),
    path("password/", PasswordView.as_view(), name="password"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", UserProfileUpdateForm.as_view(), name="profile_update"),
    path("viewhistory/", ActionListView.as_view(), name="viewhistory"),
]
