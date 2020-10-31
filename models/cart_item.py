from ._imports import *
from django.utils.translation import ugettext_lazy as _
from .cart_item_attribute import * 

class CartItemPriceMixin(models.Model):
  class Meta:
    abstract = True 
  
  def get_price(self, currency=None, price_type='price', request=None):
    if not currency:
      currency = Currency.objects.get(is_main=True)
    if price_type == 'price':
      # ціна без атрибутів без знижки
      price = self.item.get_price(currency, "price", request)
    elif price_type == 'price_with_discount':
      # ціна без атрибутів з знижкою
      price = self.item.get_price(currency, "price_with_discount", request)
    elif price_type == 'price_with_attributes':
      # ціна з атрибутами без знижки
      price = self.item.get_price(currency,  "price", request)
      price += self.get_price_of_attributes(currency, request)
    elif price_type == 'price_with_discount_with_attributes':
      # ціна з атрибутами з знижкою
      price = self.item.get_price(currency,"price_with_discount", request)
      price += self.get_price_of_attributes(currency, request)
    elif price_type == 'price_with_coupons':
      # ціна з купонами 
      price = self.item.get_price(currency, "price_with_coupons", request)
    elif price_type == 'price_with_coupons_with_discount':
      # ціна з купонами з знижкою
      price = self.item.get_price(currency, "price_with_coupons_with_discount", request)
    elif price_type == 'price_with_coupons_with_attributes':
      # ціна з купонами з атрибутами
      price = self.item.get_price(currency, "price_with_coupons", request)
      price += self.get_price_of_attributes(currency, request) 
    elif price_type == 'price_with_coupons_with_attributes_with_discount':
      # ціна з купонами з атрибутами з знижкою 
      price = self.item.get_price(currency, "price_with_coupons_with_discount", request)
      price += self.get_price_of_attributes(currency, request) 
    elif price_type == 'attributes':
      # ціна атрибутів
      price = self.get_price_of_attributes(currency, request)
    elif price_type == 'discount':
      # ціна знижки
      price = self.item.get_discount_price()
    elif price_type == 'coupons':
      # ціна купонів
      price = self.item.get_coupons_price(self.item.currency, request)
    elif price_type == 'total_price':
      # сумарна ціна без атрибутів без знижки
      price = self.item.get_price(currency, "price", request) * self.quantity
    elif price_type == 'total_price_with_discount':
      # сумарна ціна без атрибутів з знижкою
      price = self.item.get_price(currency, "price_with_discount", request) * self.quantity
    elif price_type == 'total_price_with_attributes':
      # сумарна ціна з атрибутами без знижки
      price = self.item.get_price(currency, "price", request) * self.quantity
      price += self.get_price_of_attributes(currency, request) * self.quantity 
    elif price_type == 'total_price_with_discount_with_attributes':
      # сумарна ціна з атрибутами з знижкою
      price = self.item.get_price(currency, "price_with_discount", request) * self.quantity
      price += self.get_price_of_attributes(currency, request) * self.quantity 
    elif price_type == 'total_price_with_coupons':
      # сумарна ціна з купонами 
      price = self.item.get_price(currency, "price_with_coupons", request) * self.quantity 
    elif price_type == 'total_price_with_coupons_with_discount':
      # сумарна ціна з купонами з знижкою
      price = self.item.get_price(currency, "price_with_coupons_with_discount", request) * self.quantity
    elif price_type == 'total_price_with_coupons_with_attributes':
      # сумарна ціна з купонами з атрибутами
      price = self.item.get_price(currency, "price_with_coupons_with_discount", request) * self.quantity
      price += self.get_price_of_attributes(currency, request) * self.quantity
    elif price_type == 'total_price_with_coupons_with_attributes_with_discount':
      # сумарна ціна з купонами з атрибутами з знижкою
      price = self.item.get_price(currency, "price_with_coupons_with_attributes_with_discount", request) * self.quantity
      price += self.get_price_of_attributes(currency, request) * self.quantity
    elif price_type == 'total_attributes':
      # сумарна ціна атрибутів
      price = self.get_price_of_attributes(currency, request) * self.quantity
    elif price_type == 'total_discount':
      # сумарна ціна знижки
      price = self.item.get_discount_price() * self.quantity 
    elif price_type == 'total_coupons':
      # сумарна ціна купонів 
      price = self.item.get_coupons_price(self.item.currency, request) * self.quantity 
    # curr_from = self.item.currency
    # curr_to   = currency
    # koef = currency.convert(curr_from=curr_from, curr_to=curr_to)
    # price = price * koef
    return price 

  def get_price_of_attributes(self, currency, request):
    price = 0
    for cart_item_attribute in CartItemAttribute.objects.filter(cart_item=self):
      for value in cart_item_attribute.values.all():
        # attr_price = float(value.price)
        attr_price = float(value.get_price(currency, request))
      if cart_item_attribute.value:
        # attr_price = float(cart_item_attribute.value.price)
        attr_price = float(cart_item_attribute.value.get_price(currency, request))
      price += attr_price * currency.convert(curr_from=self.item.currency, curr_to=currency)
    return price 

  # old 

  @property
  def total_price(self):
    total_price = float(self.price_of_quantity) + float(self.price_of_attributes)
    return total_price 

  @property
  def price_of_quantity(self):
    total_price = self.price_per_item * self.quantity
    return total_price
  
  @property
  def price_of_attributes(self):
    price = 0
    for cart_item_attribute in CartItemAttribute.objects.filter(cart_item=self):
      for value in cart_item_attribute.values.all():
        price += float(value.price)
      if cart_item_attribute.value:
        price += float(cart_item_attribute.value.price)
    return price 

  @property
  def price_per_item(self):
    price_per_item = self.item.get_cart_price()
    attrs = self.get_attributes().aggregate(Sum('price'))['price__sum']
    if attrs:
      price_per_item += attrs
    return price_per_item 

  @property
  def currency(self):
    return self.cart.currency

  def get_currency(self):
    return self.cart.get_currency()


class CartItem(CartItemPriceMixin):
  ordered  = models.BooleanField(
     verbose_name=("Замовлено"), default=False,
    )
  cart     = models.ForeignKey(  
     to='sw_cart.Cart',   verbose_name=("Корзина"), on_delete=models.CASCADE, blank=True, null=True, related_name="items",
    )
  order    = models.ForeignKey(  
     to='sw_order.Order', verbose_name=('Замовлення'),   on_delete=models.CASCADE, blank=True, null=True, related_name="cart_items",
    )
  item     = models.ForeignKey(  
     to="sw_catalog.Item",   verbose_name=('Товар'),   
     on_delete=models.CASCADE, 
     blank=False, null=False, 
     related_name="cart_items",
    )
  quantity = models.IntegerField(
    verbose_name=_('Кількість'), default=1,
  )
  created  = models.DateTimeField(
    verbose_name=_('Дата создания'),  default=timezone.now
  )
  updated  = models.DateTimeField(
    verbose_name=_('Дата обновления'),auto_now_add=False, 
    auto_now=True,  blank=True, null=True
  )
  
  def get_attributes(self):
    return CartItemAttribute.objects.filter(cart_item=self)

  def get_attribute(self, attr_code):
    try:
        attr = CartItemAttribute.objects.get(
            cart_item=self,
            attribute_name=ItemAttribute.objects.get(item=self.item,attribute__code=attr_code),
        ) 
    except:
        attr = None 
    return attr 

  def __str__(self):
    return f'''
      {self.item.title}, {self.quantity}, {self.total_price} {self.item.currency}
      {self.get_attributes()}
    '''

  class Meta: 
    verbose_name = _('Товар в корзині')
    verbose_name_plural = _('Товари в корзині')

