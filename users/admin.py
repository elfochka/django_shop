from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = 'first_name', 'middle_name', 'last_name', 'phone', 'email'
    fieldsets = [
        ('User data', {
            'fields': ('first_name', 'middle_name', 'last_name', 'phone', 'email')
        }),
        ("User image", {
            'fields': ('image',),
            'classes': ("collapse",),
        })
    ]
