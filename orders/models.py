from django.db import models

from users.models import CustomUser
from products.models import ProductPosition


class Deliver(models.Model):
    """Model for storing delivery options."""

    title = models.CharField(
        verbose_name="название",
        max_length=512,
    )

    price = models.DecimalField(
        verbose_name="цена",
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "доставка"
        verbose_name_plural = "доставки"

    def __str__(self):
        return self.title


class Order(models.Model):
    """Model for storing orders."""

    PAYMENT_CHOICES = (
        ("online", "Онлайн картой"),
        ("someone", "Онлайн со случайного чужого счета"),
    )

    STATUS_CHOICES = (
        ("created", "Сформирован"),
        ("unpaid", "Не оплачен"),
        ("paid", "Оплачен"),
        ("shipped", "В пути"),
        ("delivered", "Доставлен"),
        ("returned", "Возвращен"),
    )

    client = models.ForeignKey(
        CustomUser,
        verbose_name="клиент",
        on_delete=models.CASCADE,
    )
    delivery = models.ForeignKey(
        Deliver,
        verbose_name="доставка",
        on_delete=models.SET_NULL,
        null=True,
    )
    payment = models.CharField(
        verbose_name="способ оплаты",
        max_length=10,
        choices=PAYMENT_CHOICES,
    )
    status = models.CharField(
        verbose_name="статус заказа",
        choices=STATUS_CHOICES,
        default="created",
        max_length=10,
    )
    name = models.CharField(
        verbose_name="имя",
        max_length=255,
    )
    phone = models.CharField(
        verbose_name="телефон",
        max_length=11,
    )
    email = models.EmailField(verbose_name="электронная почта")
    city = models.CharField(
        verbose_name="город",
        max_length=255,
    )
    address = models.CharField(
        verbose_name="адрес",
        max_length=512,
    )
    comment = models.CharField(
        verbose_name="комментарий к заказу",
        max_length=512,
        blank=True,
        null=True,
    )
    is_paid = models.BooleanField(
        verbose_name="оплачен",
        default=False,
    )
    is_deleted = models.BooleanField(
        verbose_name="удален",
        default=False,
    )
    created = models.DateTimeField(
        verbose_name="создан",
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name="обновлен",
        auto_now=True,
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    """Model for storing order items."""

    order = models.ForeignKey(
        Order,
        verbose_name="заказ",
        on_delete=models.CASCADE,
    )
    product_position = models.ForeignKey(
        ProductPosition,
        verbose_name="позиция товара",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        verbose_name="цена",
        max_digits=10,
        decimal_places=2,
    )
    quantity = models.PositiveIntegerField(verbose_name="количество")

    class Meta:
        verbose_name = "позиция заказа"
        verbose_name_plural = "позиции заказа"

    def __str__(self):
        return f"Order {self.order.id}, Product: {self.product_position.title}"
