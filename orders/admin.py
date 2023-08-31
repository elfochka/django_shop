from django.contrib import admin

from .models import Deliver, Order, OrderItem


@admin.register(Deliver)
class DeliverAdmin(admin.ModelAdmin):
    model = Deliver
    list_display = ["title", "price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = [
        "id",
        "client",
        "delivery",
        "payment",
        "status",
        "name",
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
