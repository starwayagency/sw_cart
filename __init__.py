from django import apps 


class CartConfig(apps.AppConfig):
    name = 'box.apps.sw_shop.sw_cart'
    verbose_name = "корзина"

default_app_config = 'box.apps.sw_shop.sw_cart.CartConfig'


