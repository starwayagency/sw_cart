from django import apps 


class CartConfig(apps.AppConfig):
    name = 'sw_cart'
    verbose_name = "корзина"

default_app_config = 'sw_cart.CartConfig'


