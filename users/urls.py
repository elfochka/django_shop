from django.urls import path

from users.views import (
    AccountDetailView,
    ActionListView,
    EmailView,
    PasswordView,
    ProfileView,
    UserProfileUpdateForm,
)

app_name = "users"

urlpatterns = [
    path("account/", AccountDetailView.as_view(), name="account"),
    path("e-mail/", EmailView.as_view(), name="e-mail"),
    path("password/", PasswordView.as_view(), name="password"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", UserProfileUpdateForm.as_view(), name="profile_update"),
    path("viewhistory/", ActionListView.as_view(), name="viewhistory"),
]
