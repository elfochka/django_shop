from django.db import models
from django.templatetags.static import static

from users.models import CustomUser


def get_default_image():
    return "default_images/default.jpg"


class Category(models.Model):
    """Describes product category in eshop."""

    title = models.CharField(
        verbose_name="название",
        max_length=512,
    )
    parent = models.ForeignKey(
        verbose_name="родительская категория",
        to="Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )
    image = models.FileField(
        verbose_name="иконка (в SVG)",
        upload_to="categories/icons/",
    )
    is_chosen = models.BooleanField(
        verbose_name="избранная",
        default=False,
    )
    is_deleted = models.BooleanField(
        verbose_name="удалена",
        default=False,
    )

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
        ]
        verbose_name = "категория"
        verbose_name_plural = "категории"

    @classmethod
    def get_featured_categories(cls):
        return cls.objects.filter(is_chosen=True)[:3]

    def __str__(self):
        return self.title if not self.parent else f"{self.parent.title} / {self.title}"


class Tag(models.Model):
    """Represents a tag assigned to a product."""

    title = models.CharField(
        verbose_name="название",
        max_length=32,
    )

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
        ]
        verbose_name = "тэг"
        verbose_name_plural = "тэги"

    def __str__(self):
        return self.title


class Product(models.Model):
    """Describes a product for sale in eshop."""

    title = models.CharField(
        verbose_name="название",
        max_length=512,
    )
    description = models.TextField(
        verbose_name="описание",
        blank=True,
    )
    category = models.ForeignKey(
        verbose_name="категория",
        to=Category,
        related_name="products",
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(
        verbose_name="тэги",
        to=Tag,
        related_name="products",
        blank=True,
    )
    features = models.JSONField(
        verbose_name="характеристики",
        null=True,
        blank=True,
    )
    is_chosen = models.BooleanField(
        verbose_name="избранный",
        default=False,
    )
    is_limited = models.BooleanField(
        verbose_name="ограниченный",
        default=False,
    )
    is_deleted = models.BooleanField(
        verbose_name="удалён",
        default=False,
    )
    created = models.DateTimeField(
        verbose_name="создан",
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name="обновлён",
        auto_now=True,
    )

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["title"]),
            models.Index(fields=["-created"]),
        ]
        verbose_name = "товар"
        verbose_name_plural = "товары"

    @classmethod
    def get_popular_products(cls):
        return cls.objects.filter(is_deleted=False).order_by("?")[:8]

    @classmethod
    def get_limited_edition_products(cls):
        return cls.objects.filter(is_limited=True, is_deleted=False).order_by("?")[:16]

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """Represents one of product photos."""

    product = models.ForeignKey(
        verbose_name="товар",
        to=Product,
        related_name="images",
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name="название изображения",
        max_length=512,
    )
    image = models.ImageField(
        verbose_name="изображение",
        upload_to="images/products/",
    )

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["id"]),
        ]
        verbose_name = "изображение товара"
        verbose_name_plural = "изображения товаров"

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        """
        Return image URL if image file exists.

        Otherwise, return URL of the static product image placeholder.
        """
        try:
            url = (
                self.image.url
                if self.image.storage.exists(self.image.file.name)
                else ""
            )
        except FileNotFoundError:
            url = static("/assets/img/product-placeholder.png")
        return url


class Offer(models.Model):
    """Represents an offer (discount) in the shop."""

    class Types(models.TextChoices):
        DISCOUNT_PERCENT = "DP", "Процент скидки"
        DISCOUNT_AMOUNT = "DA", "Сумма скидки"
        FIXED_PRICE = "FP", "Фиксированная стоимость"

    products = models.ManyToManyField(
        verbose_name="товары",
        to=Product,
        related_name="offers",
        blank=True,
    )
    categories = models.ManyToManyField(
        verbose_name="категории",
        to=Category,
        related_name="offers",
        blank=True,
    )
    description = models.TextField(
        verbose_name="описание",
        blank=True,
    )
    priority = models.PositiveIntegerField(
        verbose_name="приоритет",
        blank=False,
        null=False,
        default=0,
    )
    discount_type = models.CharField(
        verbose_name="механизм скидки",
        max_length=2,
        choices=Types.choices,
        default=Types.DISCOUNT_PERCENT,
    )
    discount_value = models.PositiveIntegerField(
        verbose_name="размер скидки (руб. или %)",
    )
    date_start = models.DateField(
        verbose_name="дата начала",
        blank=True,
        null=True,
    )
    date_end = models.DateField(
        verbose_name="дата завершения",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name="активна",
        default=False,
    )
    created = models.DateTimeField(
        verbose_name="создана",
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name="обновлена",
        auto_now=True,
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["-created"]),
        ]
        verbose_name = "скидка"
        verbose_name_plural = "скидки"

    def __str__(self):
        return self.description[:64]


class AdBanner(models.Model):
    image = models.ImageField(
        upload_to="media/banners/",
        verbose_name="баннер",
        default=get_default_image
    )
    is_chosen = models.BooleanField(
        default=False,
        verbose_name="активен"
    )
    link = models.URLField(
        max_length=200,
        verbose_name="ссылка"
    )
    title = models.TextField(
        null=False, blank=False,
        verbose_name="название"
    )
    content = models.TextField(
        null=False, blank=False,
        verbose_name="контент"
    )

    class Meta:
        verbose_name = "баннер"
        verbose_name_plural = "баннеры"

    @classmethod
    def get_banners(cls):
        return cls.objects.filter(is_chosen=True)


class Review(models.Model):
    product = models.ForeignKey(
        verbose_name="товар",
        to=Product,
        related_name="reviews",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    author = models.ForeignKey(
        verbose_name="автор",
        to=CustomUser,
        related_name="reviews",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    body = models.TextField(
        verbose_name="описание",
        blank=False,
        null=False,
    )
    created = models.DateTimeField(
        verbose_name="создан",
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name="обновлён",
        auto_now=True,
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["-created"]),
        ]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
