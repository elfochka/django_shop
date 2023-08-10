from django.urls import path

from users.views import (AccountDetailView, ActionListView, EmailView,
                         PasswordView, UserUpdateView)

app_name = "users"

urlpatterns = [
    path("account/", AccountDetailView.as_view(), name="account"),
    path("e-mail/", EmailView.as_view(), name="e-mail"),
    path("password/", PasswordView.as_view(), name="password"),
    path("profile/<int:pk>/", UserUpdateView.as_view(), name="profile"),
    path("viewhistory/", ActionListView.as_view(), name="viewhistory"),
]
