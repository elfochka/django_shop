from django.urls import path

from users.views import (AccountDetailView, ActionListView, EmailView,
                         LoginView, PasswordView, ProfileView, RegisterView,
                         UserProfileUpdateForm)

app_name = "users"
urlpatterns = [
    path("account/", AccountDetailView.as_view(), name="account"),
    path("registration/", RegisterView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("e-mail/", EmailView.as_view(), name="e-mail"),
    path("password/", PasswordView.as_view(), name="password"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", UserProfileUpdateForm.as_view(), name="profile_update"),
    path("viewhistory/", ActionListView.as_view(), name="viewhistory"),
]
