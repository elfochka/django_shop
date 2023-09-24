from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeFormAdmin
from .models import Action, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeFormAdmin
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

    add_fieldsets = (
        (None, {
            "fields": ("username", "email", "password1", "password2"),
        }),
    )


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ["user", "verb", "target", "created"]
    list_filter = ["created"]
    search_fields = ["verb"]
