from django.urls import path, include

from core.views import (
    ActionListView,
)

app_name = 'core'
urlpatterns = [
    path('viewhistory/', ActionListView.as_view(), name='viewhistory'),
]
