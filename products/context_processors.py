"""
Contains context processor to put Cart into context.

More on built-in context processors:
https://docs.djangoproject.com/en/4.2/ref/templates/api/#built-in-template-context-processors
"""
from django.http import HttpRequest

from products.cart import Cart


def cart(request: HttpRequest) -> dict:
    """
    Instantiate the cart object and make it available to all templates as a variable named "cart".
    Use `{{ cart|length }}` in templates to show number of products in the cart.
    Context processors are executed in all the requests that use RequestContext.

    It will be executed every time a template is rendered using Django’s RequestContext.
    https://docs.djangoproject.com/en/4.2/ref/templates/api/#django.template.RequestContext
    """
    return {
        "cart": Cart(request),
    }
