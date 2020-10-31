from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from box.apps.sw_shop.sw_catalog.models import Item
from box.apps.sw_shop.sw_cart.models import CartItem, FavourItem, Cart 
from box.apps.sw_shop.sw_cart.utils import get_cart, get_cart_info
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json 
from .serializers import *

@api_view(['GET','POST'])
def check_if_item_with_attributes_is_in_cart(request):
  return Response(data={}, status=200)


@api_view(['GET','POST'])
def change_item_amount(request, id):
  get_cart(request).change_item_amount(id, request.data['quantity'])
  return Response(get_cart_info(request), status=203)


@api_view(['GET','POST','DELETE'])
def cart_items(request):
  cart       = get_cart(request)
  if request.method == 'GET':
    return Response(data=get_cart_info(request),status=200)
  if request.method == 'POST':
    query      = request.data
    quantity   = query.get('quantity', 1)
    item_id    = query['item_id']
    attributes = query.get('attributes', [])
    if attributes:
      attributes = json.loads(attributes)
    cart.add_item(item_id, quantity, attributes)
    return Response(data=get_cart_info(request), status=203)
  if request.method == 'DELETE':
    cart.clear()
    return Response(data=get_cart_info(request), status=204)


from box.core.sw_currency.models import Currency


@api_view(['GET','PATCH','DELETE'])
def cart_item(request, id):
  cart = get_cart(request)
  if request.method == 'GET':
    cart_item = CartItem.objects.get(id=id)
    return Response(data=CartItemSerializer(cart_item, context={'request':request}).data, status=200)
  elif request.method == 'PATCH':
    cart_item    = cart.change_cart_item_amount(id, request.data['quantity'])
    currency = None 
    currency_code = request.session.get('current_currency_code')
    if currency_code:
      currency = Currency.objects.get(code=currency_code)
    cart_item_total_price = cart_item.get_price(currency, 'total_price_with_discount_with_attributes')
    # cart_item_total_price = cart_item.total_price
    response     = {
      "cart_item_total_price":cart_item_total_price, 
    }
    response.update(get_cart_info(request))
    return Response(data=response, status=202)
  elif request.method == 'DELETE':
    get_cart(request).remove_cart_item(id)
    response = get_cart_info(request)
    return Response(response, status=200)


@api_view(['GET','POST','DELETE'])
def favour_items(request):
  cart = get_cart(request)
  if request.method == 'GET':
    favours  = FavourItem.objects.filter(cart=cart)
    response = FavourItemSerializer(favours, many=True).data
    return Response(response, status=200)
  if request.method == 'POST':
    item_id   = request.data['item_id']
    favour, _ = FavourItem.objects.get_or_create(
      cart=cart, 
      item=Item.objects.get(id=item_id)
    )
    print(favour.item)
    return Response(status=202)
  if request.method == 'DELETE':
    FavourItem.objects.filter(cart=cart).delete()
    return Response(status=204)


@api_view(['GET','DELETE'])
def favour_item(request, id):
  cart = get_cart(request)
  if request.method == 'GET':
    favour_item = FavourItem.objects.get(id=id)
    response    = FavourItemSerializer(favour_item).data
    return Response(response, status=200)
  elif request.method == 'DELETE':
    FavourItem.objects.get(id=id).delete()
    return Response(status=204)


@api_view(['DELETE'])
def remove_favour_by_like(request, id):
  FavourItem.objects.get(cart=get_cart(request), item__id=id).delete()
  return Response(status=204)


@api_view(['POST'])
def add_favour_to_cart(request, id):
  favour_item = FavourItem.objects.get(id=id)
  cart_item, _ = CartItem.objects.get_or_create(
    cart=get_cart(request),
    item=favour_item.item,
    ordered=False,
  )
  if _: cart_item.quantity = 1
  if not _: cart_item.quantity += 1
  cart_item.save()
  favour_item.delete()
  return Response(status=202)


@api_view(['POST'])
def add_favours_to_cart(request):
  favours = FavourItem.objects.filter(cart=get_cart(request))
  for favour in favours:
    cart_item, _ = CartItem.objects.get_or_create(
      cart=get_cart(request),
      item=favour.item,
      ordered=False,
    )
    if _: cart_item.quantity = 1
    if not _: cart_item.quantity += 1
    cart_item.save()
    favour.delete()
  return Response(status=200)




@api_view(['GET'])
def get_favours_amount(request):
  favours = FavourItem.objects.filter(cart=get_cart(request))
  return HttpResponse(favours.count())



# old 

# @csrf_exempt
# def get_cart_items(request):
#   return JsonResponse(get_cart_info(request))

# @api_view(['GET','POST'])
# def add_cart_item(request):
#   # query      = request.data 
#   query      = request.POST or request.GET
#   cart       = get_cart(request)
#   # print("query::",query)
#   quantity   = query.get('quantity', 1)
#   item_id    = query['item_id']
#   attributes = json.loads(query.get('attributes', []))
#   # print(attributes)
#   cart.add_item(item_id, quantity, attributes)
#   return JsonResponse(get_cart_info(request))


# @csrf_exempt
# def remove_cart_item(request):
#   cart         = get_cart(request)
#   query        = request.POST or request.GET
#   cart_item_id = query['cart_item_id']
#   cart.remove_cart_item(cart_item_id)
#   return JsonResponse(get_cart_info(request))


# @csrf_exempt
# def change_cart_item_amount(request):
#   query = request.POST or request.GET
#   cart_item_id = query['cart_item_id']
#   quantity     = query['quantity']
#   cart         = get_cart(request)
#   cart_item    = cart.change_cart_item_amount(cart_item_id, quantity)
#   response     = {
#     "cart_item_id":cart_item_id,
#     "cart_item_total_price":cart_item.total_price,
#   }
#   response.update(get_cart_info(request))
#   return JsonResponse(response)




# @csrf_exempt
# def clear_cart(request):
#   cart = get_cart(request)
#   cart.clear()
#   return JsonResponse(get_cart_info(request))



# @csrf_exempt
# def get_favours(request):
#   favours = FavourItem.objects.filter(
#     cart=get_cart(request),
#   )
#   serializer = FavourItemSerializer(favours, many=True)
#   response = {
#     'favours':serializer.data, 
#   }
#   return JsonResponse(response)





# @csrf_exempt
# def add_favour(request):
#   query           = request.POST or request.GET
#   item_id         = query['item_id']
#   favour, created = FavourItem.objects.get_or_create(
#     cart=get_cart(request),
#     item=Item.objects.get(pk=int(item_id))
#   )
#   return HttpResponse()


# @csrf_exempt
# def remove_favour(request):
#   query = request.POST or request.GET
#   favour_id = query['favour_id']
#   favour_item = FavourItem.objects.get(
#     cart=get_cart(request),
#     id=favour_id,
#   )
#   item_id = favour_item.item.id
#   favour_item.delete()
#   return HttpResponse(item_id)




# @csrf_exempt
# def remove_favour_by_like(request):
#   query   = request.POST or request.GET
#   item_id = query['item_id']
#   FavourItem.objects.get(
#     cart=get_cart(request), 
#     item=Item.objects.get(pk=int(item_id))
#   ).delete()
#   return HttpResponse()


# @csrf_exempt
# def add_favour_to_cart(request):
#   query        = request.POST or request.GET
#   item_id      = query['item_id']
#   favour_id    = query['favour_id']
#   cart_item, _ = CartItem.objects.get_or_create(
#     cart=get_cart(request),
#     item=Item.objects.get(id=item_id),
#     ordered=False,
#   )
#   quantity = 1
#   if _: cart_item.quantity = int(quantity)
#   if not _: cart_item.quantity += int(quantity)
#   cart_item.save()
#   favouritem = FavourItem.objects.get(id=favour_id)
#   favouritem.delete()
#   return HttpResponse('ok')


# @csrf_exempt
# def add_favours_to_cart(request):
#   favours = FavourItem.objects.filter(cart=get_cart(request))
#   for favour in favours:
#     cart_item, created = CartItem.objects.get_or_create(
#       cart=get_cart(request),
#       item=Item.objects.get(id=favour.item.id),
#       ordered=False,
#     )
#     quantity = 1
#     if created: cart_item.quantity = int(quantity)
#     if not created: cart_item.quantity += int(quantity)
#     cart_item.save()
#     favour.delete()
#   return HttpResponse('ok')


# @csrf_exempt
# def get_favours_amount(request):
#   favours = FavourItem.objects.filter(cart=get_cart(request))
#   return HttpResponse(favours.count())



