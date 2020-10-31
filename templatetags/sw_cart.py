from django import template
from sw_shop.sw_cart.utils import get_cart
from sw_shop.sw_cart.models import CartItemAttribute
from sw_shop.sw_catalog.models import (
    ItemAttributeValue, ItemAttribute, Attribute,
)


register = template.Library()


@register.simple_tag
def get_cart_item_attribute(cart_item, attr_code):
    # print('get_cart_item_attribute:')
    return cart_item.get_attribute(attr_code)


