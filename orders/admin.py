from django.contrib import admin
from django.contrib.admin import StackedInline

from .models import Deliver, Order, OrderItem


@admin.register(Deliver)
class DeliverAdmin(admin.ModelAdmin):
    model = Deliver
    list_display = ["title", "price", "free_threshold", "is_express"]


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
        "total_price",
    ]
    list_filter = [
        "status",
        "is_paid",
    ]
    readonly_fields = [
        "created",
        "updated",
        "total_price",
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
                    "total_price",
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
                    "delivery_price",
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
