from .models import CartItem
from catalog.models import Product
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from decimal import *
# return all items from the current user's cart
def get_cart_items(request):
	return CartItem.objects.filter(cart_session=request.session.session_key)

# add an item to the cart
def add_to_cart(request):
	postdata = request.POST.copy()
	# get product slug from post data, return blank if empty
	product_slug = postdata.get('product_slug','')
	# get quantity added, return 1 if empty
	quantity = postdata.get('quantity',1)
	# fetch the product or return a missing page error
	p = get_object_or_404(Product, slug=product_slug)
	#get products in cart
	cart_products = get_cart_items(request)
	product_in_cart = False
	# check to see if item is already in cart
	for cart_item in cart_products:
		if cart_item.product.id == p.id:
			# update the quantity if found
			cart_item.augment_quantity(quantity)
			product_in_cart = True

	if not product_in_cart:
	# create and save a new cart item
		ci = CartItem()
		ci.product = p
		ci.quantity = quantity
		ci.cart_session=request.session.session_key
		ci.save()
# returns the total number of items in the user's cart
def cart_distinct_item_count(request):
	return get_cart_items(request).count()

def cart_subtotal(request):
	cart_products = get_cart_items(request)
	subtotal=Decimal('0')

	for cp in cart_products:
		subtotal+=cp.total()
	return subtotal