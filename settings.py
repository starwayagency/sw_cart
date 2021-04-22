from django.conf import settings


def get(value, default):
    return getattr(settings, value, default)


SW_CART_OBJECTS = {
    "Cart": "astro.models.Cart",
}

SW_CART_OBJECTS = get('SW_CART_OBJECTS', DEFAULT_SW_CART_OBJECTS)
