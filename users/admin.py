from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Action, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "is_staff",
    ]
    # Which fields to show when editing user via admin panel:
    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительные поля",
            {
                "fields": (
                    "middle_name",
                    "image",
                    "phone",
                )
            },
        ),
    )
    # Which fields to show when creating user via admin panel:
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Дополнительные поля",
            {
                "fields": (
                    "middle_name",
                    "image",
                    "phone",
                )
            },
        ),
    )


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ["user", "verb", "target", "created"]
    list_filter = ["created"]
    search_fields = ["verb"]
