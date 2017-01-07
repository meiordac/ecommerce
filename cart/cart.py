from decimal import Decimal
from django.shortcuts import get_object_or_404

from catalog.models import Product
from .models import CartItem

def get_cart_items(request):
    """ return all items from the current user's cart """
    return CartItem.objects.filter(cart_session=request.session.session_key)

def add_to_cart(request):
    """ add an item to the cart """
    postdata = request.POST.copy()
    # get product slug from post data, return blank if empty
    product_slug = postdata.get('product_slug', '')
    # get quantity added, return 1 if empty
    quantity = postdata.get('quantity', 1)
    # fetch the product or return a missing page error
    product = get_object_or_404(Product, slug=product_slug)
    #get products in cart
    cart_products = get_cart_items(request)
    product_in_cart = False
    # check to see if item is already in cart
    for cart_item in cart_products:
        if cart_item.product.id == product.id:
            # update the quantity if found
            cart_item.augment_quantity(quantity)
            product_in_cart = True

    if not product_in_cart:
    # create and save a new cart item
        cartitem = CartItem()
        cartitem.product = product
        cartitem.quantity = quantity
        cartitem.cart_session = request.session.session_key
        cartitem.save()


def remove_from_cart(request, product_slug):
    """ removes an item to the cart """
    product = get_object_or_404(Product, slug=product_slug)
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        if cart_item.product.id == product.id:
            cart_item.delete()

def cart_distinct_item_count(request):
    """ returns the total number of items in the user's cart """
    return get_cart_items(request).count()

def cart_subtotal(request):
    """ Returns cart subtotal"""
    cart_products = get_cart_items(request)
    subtotal = Decimal('0')

    for cartproduct in cart_products:
        subtotal += cartproduct.total()
    return subtotal
