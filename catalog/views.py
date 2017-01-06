from django.core import urlresolvers
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect

from .models import Comment
from cart import cart
from cart.forms import ProductAddToCartForm
from .forms import CommentForm

from .models import Product, Category, Comment

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories' : categories}
    return render(request, 'index.html', context)

def about(request):
    """ Returns the about view """
    context = {}
    return render(request, 'about.html', context)

def contact(request):
    """ Returns the contact view """
    context = {}
    return render(request, 'contact.html', context)

def show_category(request, category_slug):
    """ View that returns a specific category """
    category = get_object_or_404(Category, slug=category_slug)
    products = category.product_set.all()
    categories = Category.objects.all()
    context = {'category': category, 'products': products, 'categories' : categories}
    return render(request, 'category.html', context)

def add_comment_to_product(request, product_slug):
    """ adds a comment to a product """
    product = get_object_or_404(Product, slug=product_slug)
    comment = Comment()
    comment.text = request.POST.get('text')
    comment.stars = request.POST.get('stars')
    comment.product = product
    comment.author = request.user.username
    comment.save()
    return redirect('show_product', product_slug=product_slug)

def add_to_cart(request):
    """ adds a product to cart """
    # add to cart...create the bound form
    postdata = request.POST.copy()
    form = ProductAddToCartForm(request, postdata)
    #check if posted data is valid
    if form.is_valid():
        #add to cart and redirect to cart page
        cart.add_to_cart(request)
    # if test cookie worked, get rid of it
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    print redirect('cart.views.show_cart')
    return redirect('cart.views.show_cart')



def show_product(request, product_slug):
    """ View that returns a specific product """
    product = get_object_or_404(Product, slug=product_slug)

    if request.method == 'POST' and 'add-cart' in request.POST:
        add_to_cart(request)

    elif request.method == 'POST' and 'leave-review' in request.POST:
        add_comment_to_product(request, product_slug)

    form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set the test cookie on our first GET request
    request.session.set_test_cookie()
    comment_form = CommentForm()

    categories = Category.objects.all()
    context = {'categories': categories, 'product': product, 'form':form,
               'comment_form':comment_form}
    return render(request, 'product.html', context)

def search(request):
    """ Makes a search and returns all objects with certain pattern """
    query = request.GET.get('srch-term')
    allproducts = Product.objects.all()
    products = []
    for product in allproducts:
        if query.lower() in product.name.lower():
            products.append(product)

    categories = Category.objects.all()
    context = {'products': products, 'categories' : categories, 'query' : query}
    return render(request, 'search.html', context)
