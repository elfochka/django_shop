from django.contrib import admin

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
