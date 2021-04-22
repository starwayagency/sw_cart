from django.utils.translation import ugettext_lazy as _
from django.db import models 
from django.db.models import Q
from django.contrib.auth import get_user_model 
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models import Sum

from sw_catalog.models import (
  Item, Currency, Attribute, AttributeValue, ItemAttribute, ItemAttributeValue
)

import json 
import re

from sw_cart.models.cart_item import CartItem
from sw_cart.models.cart_item_attribute import CartItemAttribute


class Cart(models.Model):
    user = models.ForeignKey(
        verbose_name=_("Користувач"), to=get_user_model(), on_delete=models.SET_NULL,
        related_name='carts', blank=True, null=True,
    )
    order = models.OneToOneField(
        verbose_name=_("Замовлення"), to="sw_order.Order", blank=True, null=True,
        on_delete=models.CASCADE, related_name='cart',
    )
    ordered = models.BooleanField(
        verbose_name=_("Замовлено"), default=False,
    )
    created = models.DateTimeField(
        verbose_name=_('Дата створення'), default=timezone.now,
    )
    updated = models.DateTimeField(
        verbose_name=_('Дата оновлення'), auto_now_add=False, auto_now=True,
        blank=True, null=True,
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = _('Корзина')
        verbose_name_plural = _('Корзини')

    def create_cart_items_with_attributes(self, item, quantity, attributes):
        cart_item = CartItem.objects.create(item=item, cart=self)
        cart_item.quantity = quantity
        cart_item.save()
        CartItemAttribute.objects.filter(cart_item=cart_item).delete()
        for attribute in attributes:
            attribute_name = ItemAttribute.objects.get(id=attribute['item_attribute_id'])
            if attribute_name.is_option:
                attribute_values = ItemAttributeValue.objects.filter(id__in=attribute['item_attribute_value_ids'])
                price = 0
                for attribute_value in attribute_values:
                    price += attribute_value.price
                cart_item_attribute = CartItemAttribute.objects.create(
                    cart_item=cart_item,
                    attribute_name=attribute_name,
                    # TODO: забрати price, бо вона і так є у ItemAttributeValue
                    price=price,
                    # values         = attribute_values,
                )
                cart_item_attribute.values.add(*attribute_values)
                # cart_item_attribute.values.set(attribute_values)
            else:
                attribute_value = ItemAttributeValue.objects.get(id=attribute['item_attribute_value_id'])
                CartItemAttribute.objects.create(
                    cart_item=cart_item,
                    attribute_name=attribute_name,
                    value=attribute_value,
                    price=attribute_value.price
                    # TODO: забрати price, бо вона і так є у ItemAttributeValue
                )

    def get_cart_item(self, item, attributes):
        cart_items = CartItem.objects.filter(cart=self, item=item)
        sdf = []
        # Проходиться по всіх товарах в корзині
        for cart_item in cart_items:
            cart_item_attributes = CartItemAttribute.objects.filter(cart_item=cart_item)
            # Проходиться по всіх атрибутах присланих з фронту
            for attribute in attributes:
                item_attr = ItemAttribute.objects.get(id=attribute['item_attribute_id'])
                if item_attr.is_option:
                    item_value = ItemAttributeValue.objects.filter(id__in=attribute['item_attribute_value_ids'])
                    item_value = set(list(item_value))
                else:
                    item_value = ItemAttributeValue.objects.get(id=attribute['item_attribute_value_id'])
                # Проходиться по всіх атрибутах поточного товара в корзині
                for cart_item_attribute in cart_item_attributes:
                    cart_attr = cart_item_attribute.attribute_name
                    if item_attr.is_option:
                        cart_value = set(list(cart_item_attribute.values.all()))
                    else:
                        cart_value = cart_item_attribute.value
                    # Якшо атрибут з фронта і атрибут товара в корзині співпадають ...
                    # https://stackoverflow.com/questions/45217691/django-check-if-querysets-are-equals

                    if item_attr == cart_attr:
                        # ... а значення атрибута з фронта і атрибута товара в корзині не співпадають ...
                        if item_value != cart_value:
                            # ... то такого товара немає в корзині
                            # sdf.append({
                            #   "cart_item":cart_item,
                            #   "status":False
                            #   })
                            # Виходить з циклу
                            break
                # якшо всі товари в корзині співпадають то продовж...........
                else:
                    continue
                break
            # Якщо цикли for attribute in attributes:
            # і for cart_item_attribute in cart_item_attributes:
            # виконались без брейків, тобто
            # всі значення атрибутів товарів в корзині
            # і всі значення атрибутів присланних з фронту співпали,
            # то товар в корзині і існує і його треба вернути
            else:
                if cart_item_attributes:
                    sdf.append({
                        'cart_item': cart_item,
                        "status": True,
                    })
                    # TODO: вияснити чого не працює return cart_item
                    # return cart_item
        for i in sdf:
            if i['status'] == True:
                return i['cart_item']

    def add_item(self, item_id, quantity, attributes=[]):
        try:
            quantity = int(quantity)
        except:
            quantity = 1
        item = Item.objects.get(pk=int(item_id))
        if not attributes:
            cart_item, created = CartItem.objects.get_or_create(
                cart=self,
                item=item,
            )
            if created:
                cart_item.quantity = quantity
            elif not created:
                cart_item.quantity += quantity
            cart_item.save()
        elif attributes:
            cart_items = CartItem.objects.filter(cart=self, item=item)
            if not cart_items:
                self.create_cart_items_with_attributes(item, quantity, attributes)
            else:
                cart_item = self.get_cart_item(item, attributes)
                if cart_item:
                    cart_item.quantity += quantity
                    cart_item.save()
                else:
                    self.create_cart_items_with_attributes(item, quantity, attributes)

    def change_cart_item_amount(self, cart_item_id, quantity):
        try:
            quantity = int(quantity)
        except:
            quantity = 1
        cart_item = CartItem.objects.get(
            id=cart_item_id,
            cart=self,
        )
        cart_item.quantity = quantity
        cart_item.save()
        return cart_item

    def change_item_amount(self, item_id, quantity):
        try:
            quantity = int(quantity)
        except:
            quantity = 1
        cart_item = CartItem.objects.get(
            item__id=item_id,
            cart=self,
        )
        cart_item.quantity = quantity
        cart_item.save()
        return cart_item

    def remove_cart_item(self, cart_item_id):
        CartItem.objects.get(
            cart=self,
            id=cart_item_id,
        ).delete()

    def clear(self):
        CartItem.objects.filter(cart=self).delete()

    @property
    def items_quantity(self):
        items_quantity = 0
        for cart_item in CartItem.objects.filter(cart=self):
            items_quantity += cart_item.quantity
        return items_quantity

    @property
    def items_count(self):
        return CartItem.objects.filter(cart=self).all().count()

    # prices new

    def get_price(self, currency=None, price_type='total_price', request=None):
        from sw_order.models import OrderAdditionalPrice
        if not currency:
            currency = Currency.objects.get(is_main=True)
        if price_type == 'total_price':
            price = 0
            for cart_item in CartItem.objects.filter(cart=self):
                koef = currency.convert(curr_from=cart_item.item.currency, curr_to=currency)
                curr_from = cart_item.item.currency
                ci = cart_item.get_price(currency, "total_price_with_coupons_with_attributes_with_discount")
                # ci    = cart_item.get_price(currency, "total_price_with_discount_with_attributes")
                price += ci
                # price = price + ci*koef
            for additional_price in OrderAdditionalPrice.objects.all():
                price = price + additional_price.price * currency.convert(curr_from=self.get_currency(), curr_to=currency)
        elif price_type == 'discount':
            price = 0
            for cart_item in CartItem.objects.filter(cart=self):
                koef = currency.convert(curr_from=cart_item.item.currency, curr_to=currency)
                price += cart_item.get_price(currency, 'total_discount')
                price = price + price * koef
        elif price_type == 'total_with_discount':
            price = 0
            for cart_item in CartItem.objects.filter(cart=self):
                koef = currency.convert(curr_from=cart_item.item.currency, curr_to=currency)
                price += cart_item.get_price(currency, 'total_price_with_discount')
                # price = price + price*koef
                # ^ з цим рядком не працює
                # |
        elif price_type == 'total':
            price = 0
            for cart_item in CartItem.objects.filter(cart=self):
                koef = currency.convert(curr_from=cart_item.item.currency, curr_to=currency)
                price += cart_item.get_price(currency, 'total_price')
                # price = price + price*koef
                # ^ з цим рядком не працює
                # |
        # todo: замовлення без купону, за мовлення з купоном
        # elif price_type == '':
        #   price = price
        # elif price_type == '':
        #   price = price
        # elif price_type == '':
        #   price = price
        # elif price_type == '':
        #   price = price
        return price

    # prices old

    @property
    def total_price(self):
        from sw_order.models import OrderAdditionalPrice
        total_price = 0
        # for cart_item in self.items.all():
        for cart_item in CartItem.objects.filter(cart=self):
            if cart_item.total_price:
                total_price += cart_item.total_price
        for additional_price in OrderAdditionalPrice.objects.all():
            price = additional_price.price
            if additional_price.currency == self.currency:
                price = price
            else:
                # todo: КОНВЕРТУВАТИ ЦІНУ ДО ВАЛЮТИ
                price = price
            total_price += price
        return float(total_price)

    @property
    def currency(self):
        return Currency.objects.get(is_main=True).code

    def get_currency(self):
        return Currency.objects.get(is_main=True)
