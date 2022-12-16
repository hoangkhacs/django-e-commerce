from contextlib import nullcontext
from os import link
from django.shortcuts import render
from store.models import Product
from category.models import Category


def home(request):
    products = Product.objects.all().filter(is_available=True).order_by("-quantity")[:4]
    products_new = Product.objects.all().filter(
        is_available=True).order_by("-saled")[:4]
    products_discount = Product.objects.all().filter(
        is_available=True).order_by("-discount")[:4]
    links = Category.objects.all()
    context = {
        'products': products,
        'nodes': links,
        'products_new': products_new,
        'products_discount': products_discount
    }
    return render(request, 'home.html', context=context)


def error_404_handler(request, exception):
    return render(request, '404.html')
