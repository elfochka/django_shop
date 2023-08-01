from django.urls import path
from django.contrib.auth.views import LogoutView

from users.views import (
    AccountDetailView,
    UserRegistrationView,
    UserLoginView,
    EmailView,
    PasswordView,
    ProfileView,
    UserProfileUpdateForm,
    ActionListView,
)

app_name = "users"

urlpatterns = [
    path("account/", AccountDetailView.as_view(), name="account"),
    path('registration/', UserRegistrationView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("e-mail/", EmailView.as_view(), name="e-mail"),
    path("password/", PasswordView.as_view(), name="password"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", UserProfileUpdateForm.as_view(), name="profile_update"),
    path("viewhistory/", ActionListView.as_view(), name="viewhistory"),
]
