# from ._imports import * 
from django.db import models 
from django.utils.translation import ugettext_lazy as _


class CartItemAttribute(models.Model):
  cart_item = models.ForeignKey(
    verbose_name=_("Товар в корзині"), on_delete=models.CASCADE,
    to="sw_cart.CartItem", related_name='attributes',
  )
  attribute_name = models.ForeignKey(
    to="sw_catalog.ItemAttribute", on_delete=models.CASCADE,
    verbose_name=_("Атрибут"), unique=False,
  )
  value = models.ForeignKey(
    to="sw_catalog.ItemAttributeValue", 
    # on_delete=models.CASCADE,
    on_delete=models.SET_NULL, blank=True, null=True,
    verbose_name=_("Значення"), unique=False, related_name="cart_item_attributes",
  )
  values = models.ManyToManyField(
    to="sw_catalog.ItemAttributeValue", verbose_name=_("Значення"), blank=True
  )
  price = models.FloatField(
    verbose_name=_("Ціна"), default=0,
    # verbose_name=_("Ціна"), null=False, blank=False, default=0,
    # verbose_name=_("Ціна"), null=True, blank=True, default=0,
  )

  class Meta: 
    verbose_name = _('вибраний атрибут у товара в корзині')
    verbose_name_plural = _('вибрані атрибути у товарів в корзині')
  
  def __str__(self):
    # return f'{self.cart_item.item.title}, {self.attribute_name.name}:{self.value.value}'
    if self.attribute_name.is_option:
      return f'{self.cart_item.item.title}, {self.attribute_name.attribute.name}:{self.values.all()}'
    else:
      return f'{self.cart_item.item.title}, {self.attribute_name.attribute.name}:{self.value.value.value}'


'''
attributes: [
    {
        "item_attribute_id":int,
        "item_attribute_value_id":int, 
    },
    {
        "item_attribute_id":int,
        "item_attribute_value_id":int, 
    },
    {
        "item_attribute_id":int,
        "item_attribute_value_ids":[int,int,int,...,int],
    },
    {
        "item_attribute_id":int,
        "item_attribute_value_ids":[int,int,int,...,int],
    },
    {
        "item_attribute_id":int,
        "item_attribute_value_ids":[int,int,int,...,int], 
    },
    {
        "item_attribute_id":int,
        "item_attribute_value_ids":[int,int,int,...,int], 
    },
]
'''

