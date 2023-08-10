from random import randint

from django.core.management.base import BaseCommand

from products.models import Product


class Command(BaseCommand):
    """
    Set random product where `is_limited = True` as `is_chosen`.
    """

    help = """
    Выбирает случайный товар с флагом `is_limited = True` как "Предложение дня" (`is_chosen = True`) для отображения
    в блоке "Ограниченное предложение" на главной странице. Текущему товару "Предложение дня" (если он имеется)
    устанавливается `is_chosen = False`.
    """

    def handle(self, *args, **options):
        """
        Handles the flow of the command.
        """
        chosen_product = Product.objects.filter(is_chosen=True).first()
        if chosen_product:
            print("Текущее Предложение дня:", chosen_product)
        else:
            print("Текущее Предложение дня - не выбрано.")

        limited_products = Product.objects.filter(is_limited=True, is_chosen=False)
        limited_products_qty = limited_products.count()

        if limited_products_qty:
            new_chosen_product = limited_products[randint(0, limited_products_qty - 1)]
            new_chosen_product.is_chosen = True
            new_chosen_product.save()

            print("Установлено новое Предложение дня:", new_chosen_product)

            if chosen_product:
                chosen_product.is_chosen = False
                chosen_product.save()
        else:
            print("Предложение дня не изменено.")
