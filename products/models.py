from django.db import models

# from django.urls import reverse


class Category(models.Model):
    """
    Describes product category in eshop.
    """

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

    def __str__(self):
        return self.title if not self.parent else f"{self.parent.title} / {self.title}"


class Tag(models.Model):
    """
    Represents a tag assigned to a product.
    """

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
    """
    Describes a product for sale in eshop.
    """

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

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("shop:product_detail", args=[self.id, self.slug])


class ProductImage(models.Model):
    """
    Represents one of product photos.
    """

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
