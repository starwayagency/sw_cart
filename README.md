Change cart item quantity (using item.id)
POST "/api/cart_item/<id>/item/"
id - item.id 

Get all items in cart 
GET /api/cart_items/

Create cart item
POST /api/cart_items/
item_id: item.id 
quantity: int

Delete all cart items.
DELETE /api/cart_items/

Get cart item 
GET "/api/cart_item/<id>/"
id - cart_item.id

Change cart item quantity (using cart_item.id)
PATCH "/api/cart_item/<id>/"
quantity: int 
id - cart_item.id

Delete cart Item
DELETE "/api/cart_item/<id>/"

Get all items in favour 
GET "/api/favour_items/"

Add item to favours 
POST "/api/favour_items/"
item_id: item.id 

Delete favour item
DELETE "/api/favour_items/<id>/"
id - favour_item.id 

Remove item from favours.
DELETE "/api/favour_item/<id>/remove_by_like/"
id - item.id 

Add favour item to cart.
POST "/api/favour_item/<id>/add_to_cart/" 
id - favour_item.id

Add all favour items to cart. 
POST "/api/add_favours_to_cart/"



