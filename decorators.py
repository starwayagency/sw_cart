from functools import wraps
from django.shortcuts import redirect
from box.apps.sw_shop.sw_cart.utils import get_cart
from box.apps.sw_shop.sw_order.models import Order, CartItem


def cart_exists(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
    if not CartItem.objects.filter(cart=get_cart(request)).exists():
      return redirect('/')
    return function(request, *args, **kwargs)
  return wrap



