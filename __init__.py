from django import apps 


class CartConfig(apps.AppConfig):
    name = 'sw_shop.sw_cart'
    verbose_name = "корзина"

default_app_config = 'sw_shop.sw_cart.CartConfig'


