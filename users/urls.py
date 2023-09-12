from django.urls import path

from users.views import (AccountDetailView, ActionListView, EmailView, EmailSentView,
                         PasswordView, UserUpdateView, HistoryOrderView)

app_name = "users"

urlpatterns = [
    path("account/", AccountDetailView.as_view(), name="account"),
    path("e-mail/", EmailView.as_view(), name="e-mail"),
    path("password/", PasswordView.as_view(), name="password"),
    path("history-order/<int:pk>/", HistoryOrderView.as_view(), name="history_order"),
    path("profile/<int:pk>/", UserUpdateView.as_view(), name="profile"),
    path("viewhistory/", ActionListView.as_view(), name="viewhistory"),
]
