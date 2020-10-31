from box.apps.sw_shop.sw_cart.api.serializers import CartItemSerializer
from box.apps.sw_shop.sw_cart.models import Cart, CartItem
from box.core.sw_currency.models import Currency 

def get_cart(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id, ordered=False)
	except Exception as e:
		print(e)
		cart = Cart()
		cart.save()
		request.session['cart_id'] = cart.id
		cart = Cart.objects.get(id=cart.id, ordered=False)
	return cart


def get_cart_info(request):
  cart = get_cart(request)
  cart_items = CartItem.objects.filter(cart=cart)
  cart_items_count = cart.items_count
  cart_items_quantity = cart.items_quantity
  currency_code = request.session.get('current_currency_code', cart.currency)
  cart_currency = currency_code
  currency = Currency.objects.get(code=currency_code)
  cart_total_price = cart.get_price(currency, price_type='total_price')
  # cart_total_price = cart.total_price
  return {
    'cart_items':CartItemSerializer(cart_items, many=True, context={'request':request}).data,
    "cart_total_price":cart_total_price,
    "cart_items_count":cart_items_count,
    "cart_items_quantity":cart_items_quantity,
    "cart_currency":cart_currency,
    # ""
  }



