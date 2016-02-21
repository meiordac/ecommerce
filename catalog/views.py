from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader

from .models import Product
from .models import Category

# Create your views here.


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = { 'products': products,
    'categories' : categories }
    return render(request, 'index.html', context)

def show_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products=category.product_set.all()
    categories = Category.objects.all()
    context = {'category': category,
     'products': products,
     'categories' : categories
    }
    return render(request, 'category.html', context)

def show_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    #categories=product.categories.filter(is_active=True)
    categories = Category.objects.all()
    context = {'categories': categories,
     'product': product
    }
    return render(request, 'product.html', context)