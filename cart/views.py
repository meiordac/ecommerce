from django.shortcuts import render
from catalog.models import Category
from . import cart

def show_cart(request):
    cart_items = cart.get_cart_items(request)
    cart_subtotal = cart.cart_subtotal(request)
    categories = Category.objects.all()
    context = {'cart_items':cart_items,
               'cart_subtotal':cart_subtotal,
               'categories':categories}
    return render(request, 'cart.html', context)
