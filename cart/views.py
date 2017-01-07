from django.shortcuts import get_object_or_404, render, redirect
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

def destroy(request, product_slug):
    cart.remove_from_cart(request, product_slug)
    return redirect('show_cart')
