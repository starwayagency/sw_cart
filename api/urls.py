from django.urls import path, include 
from .views import * 


urlpatterns = [
  path('cart_items/',          cart_items,         name='cart_items'),
  path('cart_item/<id>/',      cart_item,          name='cart_item'),
  path('cart_item/<id>/item/', change_item_amount, name='change_item_amount'),
  
  path('favour_items/',             favour_items,        name='favour_items'),
  path('favour_items/add_to_cart/', add_favours_to_cart, name='add_favours_to_cart'),
  path('favour_items/amount/',      get_favours_amount,  name='get_favours_amount'),

  path('favour_item/<id>/',                favour_item,           name='favour_item'),
  path('favour_item/<id>/add_to_cart/',    add_favour_to_cart,    name='add_favour_to_cart'),
  path('favour_item/<id>/remove_by_like/', remove_favour_by_like, name='remove_favour_by_like'),
]





