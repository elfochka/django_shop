from django.contrib import admin

from .models import Deliver


@admin.register(Deliver)
class DeliverAdmin(admin.ModelAdmin):
    model = Deliver
    list_display = ["title", "price"]
