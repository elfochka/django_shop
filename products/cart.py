from decimal import Decimal

from django.conf import settings
from django.http import HttpRequest

from orders.models import Deliver
from products.models import ProductPosition


class Cart:
    """
    Describes shopping cart in eshop as `cart` dictionary in the session.
    """

    def __init__(self, request: HttpRequest):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # Create an empty cart
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(
        self,
        product_position: ProductPosition,
        quantity: int = 1,
        override_quantity: bool = False,
    ) -> None:
        """
        Add a product position to the cart or update it's quantity.
        We add product position from the product view, and override it's quantity from cart detail view.

        :param product_position: the product instance to add or update in the cart.
        :param quantity: optional integer with the product quantity.
        :param override_quantity: indicates whether the quantity needs to be overridden with the given
                                  quantity (True), or whether the quantity has to be added to the existing
                                  quantity (False).
        """
        product_position_id = str(product_position.id)

        if product_position_id not in self.cart:
            # NB: we store price with discount (if any) applied
            self.cart[product_position_id] = {
                "quantity": 0,
                "price": str(product_position.get_price_with_discount()),
            }

        if override_quantity:
            self.cart[product_position_id]["quantity"] = quantity
        else:
            self.cart[product_position_id]["quantity"] += quantity

        if self.cart[product_position_id]["quantity"] == 0:
            del self.cart[product_position_id]

        self.save()

    def save(self):
        """
        Mark the session as "modified" to make sure it gets saved.
        Reference: https://docs.djangoproject.com/en/4.2/topics/http/sessions/#when-sessions-are-saved
        """
        self.session.modified = True

    def remove(self, product_position: ProductPosition):
        """
        Remove a product_position from the cart.

        :param product_position: product_position to remove from the cart.
        """
        product_position_id = str(product_position.id)

        if product_position_id in self.cart:
            del self.cart[product_position_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the product positions from the database.
        """
        product_position_ids = self.cart.keys()
        product_positions = ProductPosition.objects.filter(
            id__in=product_position_ids
        ).select_related("product")
        cart = self.cart.copy()

        # Add database model instances to the cart
        for product_position in product_positions:
            cart[str(product_position.id)]["product_position"] = product_position

        # Iterate over the items in the cart, converting prices from str back to decimal,
        # and calculate total price for each position.
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items (i.e., sum all quantities of items) in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_delivery_price(self, delivery: Deliver):
        """Return delivery price taking into account delivery type, number of sellers and total price."""
        products_price = self.get_total_products_price()
        sellers_qty = len(set([item["product_position"].seller.pk for item in self]))

        if not delivery.is_express:
            if products_price < delivery.free_threshold or sellers_qty > 1:
                return delivery.price
            if products_price > delivery.free_threshold and sellers_qty == 1:
                return 0

        return delivery.price

    def get_total_products_price(self):
        """
        Count total price for all items in the cart.
        """
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )
