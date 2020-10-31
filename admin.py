from django.contrib import admin 
from box.apps.sw_shop.sw_cart.models import (
  Cart, CartItem, FavourItem, CartItemAttribute
)
from django.utils.html import format_html, mark_safe
from django.urls import reverse

import nested_admin



class CartItemAttributeInlineEditable(nested_admin.NestedTabularInline):
  model = CartItemAttribute
  exclude = []


class CartItemAttributeInline(nested_admin.NestedTabularInline):
  model = CartItemAttribute
  exclude = []
  # classes = ['collapse']
  def has_change_permission(self, request, obj=None):
    return False 
  def has_add_permission(self, request, obj=None):
    return False 
  def has_delete_permission(self, request, obj=None):
    return False 
  
  
class CartItemInline(nested_admin.NestedTabularInline):
    def show_item(self, obj):
      option = "change" # "delete | history | change"
      massiv = []
      obj   = obj.item
      app   = obj._meta.app_label
      model = obj._meta.model_name
      url   = f'admin:{app}_{model}_{option}'
      href  = reverse(url, args=(obj.pk,))
      name  = f'{obj.title}'
      link  = mark_safe(f"<a href={href}>{name}</a>")
      return link
    def price_per_item(self, obj):
      return obj.price_per_item
    def total_price(self, obj):
      return obj.total_price
    def has_add_permission(self, request, obj=None):
        return False 
    def has_delete_permission(self, request, obj=None):
        return False 
    # КОЛИ ЦЯ ШТУКА ВКЛЮЧЕНА - ТОВАРИ НЕ ВІДОБРАЖАЮТЬСЯ ПІД ЗАКАЗОМ
    # def has_change_permission(self, request, obj=None):
    #     return False 
    def currency(self, obj):
      return obj.currency
    currency.short_description = ("Валюта")
    show_item.short_description      = ("Товар")
    price_per_item.short_description = ("Ціна за одиницю товару")
    total_price.short_description    = ("Суммарна вартість товару")
    fields = [
      'show_item',
      'currency',
      'price_per_item',
      'quantity',
      'total_price',
      'ordered',
    ]
    readonly_fields = fields
    exclude = [
      "item",
      'cart',
    ]
    model = CartItem
    extra = 0
    inlines = [
      CartItemAttributeInline,
    ]


class CartAdmin(nested_admin.NestedModelAdmin):
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # def has_add_permission(self, request, obj=None):
    #     return False
    def show_order(self, obj):
      option = "change" # "delete | history | change"
      massiv = []
      obj   = obj.order
      if obj:
        app   = obj._meta.app_label
        model = obj._meta.model_name
        url   = f'admin:{app}_{model}_{option}'
        args  = (obj.pk,)
        href  = reverse(url, args=args)
        name  = f'{obj.id or None}'
        name = 'order'
        link  = mark_safe(f"<a href={href}>{name}</a>")
        return link
      return '---'
    def total_price(self, obj):
        return obj.total_price
    show_order.short_description = "Замовлення"
    total_price.short_description = "Суммарна вартість корзини"
    list_display = [
        'id',
        'ordered',
        'show_order',
        'created', 
        'updated',
    ]
    list_display_links = [
      'id',
      'created',
      'updated',
    ]
    readonly_fields = [
        'total_price',
        'ordered',
        "created",
        'updated',
    ]
    fields = [ 
        'total_price',
        "ordered",
        "created",
        'updated',
    ]
    inlines = [
        # CartItemInline,
    ]


class CartItemAttributeAdmin(nested_admin.NestedModelAdmin):
  pass 


class CartItemAdmin(nested_admin.NestedModelAdmin):
    list_display = [field.name for field in CartItem._meta.fields]

    exclude = [
    ]
    inlines = [
      # CartItemAttributeInlineEditable,
      CartItemAttributeInline
    ]
    readonly_fields = [
      'cart',
      'order',
      'item',
      'created',
      'ordered',
    ]
    class Meta:
        model = CartItem


class FavourItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FavourItem._meta.fields]
    exclude = [
    ]
    class Meta:
        model = FavourItem


class CartItemAttributeAdmin(admin.ModelAdmin):
  pass 


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(CartItemAttribute, CartItemAttributeAdmin)
