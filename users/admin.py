from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'phone', 'email')
    fieldsets = (
        ('User data', {
            'fields': ('first_name', 'middle_name', 'last_name', 'phone', 'email')
        }),
        ("User image", {
            'fields': ('image',),
            'classes': ("collapse",),
        }))
    ordering = ('email',)


