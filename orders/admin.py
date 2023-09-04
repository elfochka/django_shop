from django.contrib import admin
from django.contrib.admin import StackedInline

from .models import Deliver, Order, OrderItem


@admin.register(Deliver)
class DeliverAdmin(admin.ModelAdmin):
    model = Deliver
    list_display = ["title", "price"]


class OrderItemInline(StackedInline):
    model = OrderItem
    fields = [
        "product_position",
        "price",
        "quantity",
    ]
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = [
        "id",
        "client",
        "name",
        "delivery",
        "payment",
        "status",
        "is_paid",
    ]
    list_filter = [
        "status",
        "is_paid",
    ]
    readonly_fields = [
        "created",
        "updated",
    ]
    inlines = [OrderItemInline]
    fieldsets = [
        (
            "Клиент и контактные данные",
            {
                "fields": [
                    "client",
                    "name",
                    "phone",
                    "email",
                ]
            },
        ),
        (
            "Способ оплаты и статус",
            {
                "fields": [
                    "payment",
                    "status",
                    "is_paid",
                    "is_deleted",
                ]
            },
        ),
        (
            "Доставка",
            {
                "fields": [
                    "delivery",
                    "city",
                    "address",
                    "comment",
                ]
            },
        ),
        (
            "Время создания и изменения",
            {
                "fields": [
                    "created",
                    "updated",
                ]
            },
        ),
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = [
        "order",
        "product_position",
        "price",
        "quantity",
    ]
