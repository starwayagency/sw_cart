from django import template
from sw_cart.utils import get_cart
from sw_cart.models import CartItemAttribute
from sw_catalog.models import (
    ItemAttributeValue, ItemAttribute, Attribute,
)


register = template.Library()


@register.simple_tag
def get_cart_item_attribute(cart_item, attr_code):
    return cart_item.get_attribute(attr_code)


@register.simple_tag
def get_cart_item_price(cart_item, currency, price_type):
    return cart_item.get_price(currency, price_type)



@register.simple_tag
def get_cart_price(cart, currency, price_type):
    return cart.get_price(currency, price_type)


