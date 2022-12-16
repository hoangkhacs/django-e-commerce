from contextlib import redirect_stderr
from genericpath import exists
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse

from store.models import Product
from carts.models import Cart, CartItem

# Create your views here.


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def cart(request, total=0, quantity=0, cart_items=None, save=0):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user_id=request.user.id)
            cart_items = CartItem.objects.filter(
                cart=cart)
        # else:
        #     cart = Cart.objects.get(cart_id=_cart_id(request=request))
        #     cart_items = CartItem.objects.filter(cart=cart)
            for cart_item in cart_items:
                save += (cart_item.product.price*cart_item.product.discount)*cart_item.quantity;
                total += (cart_item.product.price - cart_item.product.price*cart_item.product.discount) * cart_item.quantity
                quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass    # Chỉ bỏ qua
    context = {
        'total': '{:3,}'.format(total),
        'quantity': quantity,
        'cart_items': cart_items,
        'save': '{:3,}'.format(save)
    }
    return render(request, 'store/cart.html', context=context)


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)    # Get object product
    if current_user.is_authenticated:
        try:
            cart = Cart.objects.get(user_id=request.user.id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request),
                user=request.user,
            )
            cart.save()

        if request.method == 'POST':
            if 'quantity' in request.POST:
                quantity = request.POST.get('quantity')

        is_exists_cart_item = CartItem.objects.filter(
            product=product, cart=cart).exists()
        if is_exists_cart_item:
            cart_item = CartItem.objects.get(
                product=product,
                cart=cart
            )
            cart_item.quantity += int(quantity)
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=quantity
            )
        cart_item.save()
        # return HttpResponseRedirect(reverse('product_detail'))
        # return HttpResponse("")
        return redirect('cart')
        # return render(request, 'product_detail', {'bar': bar})


def remove_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)    # Get object product
    if current_user.is_authenticated:
        cart = Cart.objects.get(user_id=request.user.id)

        is_exists_cart_item = CartItem.objects.filter(
            product=product, cart=cart).exists()
        if is_exists_cart_item:
            cart_item = CartItem.objects.get(
                product=product,
                cart=cart
            )
            if (cart_item.quantity > 1):
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=quantity
            )
        return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart = Cart.objects.get(user_id=request.user.id)
        cart_item = CartItem.objects.get(
            product=product,
            cart=cart,
        )
        cart_item.delete()
    return redirect('cart')
