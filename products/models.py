import random
from datetime import datetime

from django.db import models
from django.db.models import Avg, Max, Min, Q
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
        return cls.objects.filter(is_limited=True, is_deleted=False, is_chosen=False).order_by("?")[:16]

    def get_min_price(self):
        return self.productposition_set.aggregate(lowest_price=Min("price"))["lowest_price"]

    def get_avg_price(self):
        """Return average price of all product positions for this product, rounded to two decimal places."""
        return round(
            self.productposition_set.aggregate(average_price=Avg("price"))["average_price"],
            2,
        )

    def get_avg_price_with_discount(self):
        """
        Return average price of all product positions for this product, rounded to two decimal places,
        with maximum discount applied.
        """
        prices_with_discount = [
            position.get_price_with_discount() for position in self.productposition_set.all()
        ]
        average_price = round(sum(prices_with_discount) / len(prices_with_discount), 2)
        if average_price < 1:
            average_price = 1
        return average_price

    @property
    def get_max_price(self):
        return self.productposition_set.aggregate(highest_price=Max("price"))["highest_price"]

    @property
    def get_old_price(self):
        old_price = self.productposition_set.aggregate(Avg("price"))["price__avg"]
        if not old_price:
            return None
        return round(old_price, 2)

    # @property
    # def get_new_price_and_sale(self):
    #     offers = Offer.objects.filter(
    #         is_active=True,
    #         date_start__lte=datetime.today(),
    #         date_end__gte=datetime.today()).filter(Q(products=self) | Q(categories=self.category))
    #
    #     if self.get_old_price:
    #
    #         temp_new_price = 0
    #         new_price = False
    #         sale = False
    #         for offer in offers:
    #             if offer.discount_type == Offer.Types.DISCOUNT_PERCENT:
    #                 temp_new_price -= offer.discount_value
    #                 if (new_price and temp_new_price < new_price) or not new_price:
    #                     sale = f"-{offer.discount_value}%"
    #                     new_price = self.get_old_price - (self.get_old_price * offer.discount_value) / 100
    #             elif offer.discount_type == Offer.Types.DISCOUNT_AMOUNT:
    #                 temp_new_price = self.get_old_price - offer.discount_value
    #                 if (new_price and temp_new_price < new_price) or not new_price:
    #                     new_price = temp_new_price
    #                     sale = f"-${offer.discount_value}"
    #             elif offer.discount_type == Offer.Types.FIXED_PRICE:
    #                 new_price = offer.discount_value
    #                 sale = f"${offer.discount_value}"
    #         return {"new_price": round(new_price, 2), "sale": sale}

    @property
    def get_lowest_price_position(self):
        return self.productposition_set.order_by("price").first()

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
        banners = cls.objects.filter(is_chosen=True)
        possible_banners = random.sample(list(banners.values_list("id", flat=True)), k=3)
        random_banners = banners.filter(pk__in=possible_banners)
        return random_banners


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


class Seller(models.Model):
    title = models.CharField(
        verbose_name="Название",
        max_length=255,
    )
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="sellers/",
    )
    address = models.CharField(
        verbose_name="Адрес",
        max_length=255,
    )
    phone = models.CharField(
        verbose_name="Телефон",
        max_length=20,
    )
    email = models.EmailField(verbose_name="Email")
    created = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name="Дата обновления",
        auto_now=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"


class ProductPosition(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name="positions",
        verbose_name="Продавец",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество на складе")
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )
    free_shipping = models.BooleanField(
        verbose_name="Бесплатная доставка",
        default=False,
    )

    def __str__(self):
        return f"{self.product.title} - {self.seller.title}"

    class Meta:
        verbose_name = "Товарная позиция"
        verbose_name_plural = "Товарные позиции"

    def get_price_with_discount(self):
        """
        Return price with discount applied, or base price if there's no discounts for this product,
        rounded to two decimal positions.
        """
        price_with_discount = self.price

        # Find applicable offer with top priority
        top_offer = (
            Offer.objects.filter(
                is_active=True,
                date_start__lte=datetime.today(),
                date_end__gte=datetime.today(),
            )
            .filter(Q(products__in=[self.product]) | Q(categories__in=[self.product.category]))
            .order_by("-priority")
        ).first()
        if top_offer:
            if top_offer.discount_type == Offer.Types.DISCOUNT_PERCENT:
                price_with_discount -= (price_with_discount * top_offer.discount_value) / 100
            elif top_offer.discount_type == Offer.Types.DISCOUNT_AMOUNT:
                price_with_discount -= top_offer.discount_value
            elif top_offer.discount_type == Offer.Types.FIXED_PRICE:
                price_with_discount = top_offer.discount_value
        if price_with_discount < 1:
            price_with_discount = 1
        return round(price_with_discount, 2)
