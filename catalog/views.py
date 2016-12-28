from django.core import urlresolvers
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect

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
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.author = request.user.name
            comment.save()
            return redirect('show_product', product_slug=product_slug)

    else:
        form = CommentForm()
        return redirect('show_product', product_slug=product_slug)


def show_product(request, product_slug):
    """ View that returns a specific product """
    product = get_object_or_404(Product, slug=product_slug)
    #categories=product.categories.filter(is_active=True)
    categories = Category.objects.all()
    # need to evaluate the HTTP method
    if request.method == 'POST':
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
        url = urlresolvers.reverse('show_cart')

        return HttpResponseRedirect(url)
    # it is a GET, create the unbound form. Note request as a kwarg
    else:
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set the test cookie on our first GET request
    request.session.set_test_cookie()
    context = {'categories': categories, 'product': product, 'form':form}
    return render(request, 'product.html', context)
