from django.contrib import admin
from django.contrib.admin import TabularInline
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .models import Category, Tag, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Category.
    """

    model = Category
    list_display = [
        "title",
        "parent",
        "is_chosen",
        "is_deleted",
    ]
    ordering = [
        "id",
        "parent",
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Tag.
    """

    model = Tag
    list_display = [
        "title",
    ]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for ProductImage.
    """

    model = ProductImage
    list_display = [
        "title",
        "product",
    ]
    ordering = [
        "product",
        "id",
    ]


class ProductImageInline(TabularInline):
    """
    Inline ProductImage row with built-in image preview.
    """

    model = ProductImage
    fields = [
        "image_preview",
        "title",
        "image",
    ]
    readonly_fields = ["image_preview"]
    ordering = ["id"]
    extra = 0

    def image_preview(self, product_image: ProductImage) -> str:
        """
        Render image preview.
        """
        if product_image.image:
            return mark_safe(
                render_to_string(
                    "products/product_image_preview.html",
                    {
                        "product_image": product_image,
                    },
                )
            )
        return ""

    image_preview.short_description = "Превью"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Product.
    """

    model = Product
    list_display = [
        "title",
        "category",
        "is_chosen",
        "is_limited",
        "is_deleted",
    ]
    list_filter = [
        "is_chosen",
        "is_limited",
        "is_deleted",
    ]
    readonly_fields = [
        "created",
        "updated",
    ]
    inlines = [ProductImageInline]
    fieldsets = [
        (
            "Основная информация о товаре",
            {
                "fields": [
                    "title",
                    "category",
                ]
            },
        ),
        (
            "Описание и характеристики",
            {
                "fields": [
                    "description",
                    "features",
                    "tags",
                ]
            },
        ),
        (
            "Статусы товара",
            {
                "fields": [
                    "is_chosen",
                    "is_limited",
                    "is_deleted",
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
