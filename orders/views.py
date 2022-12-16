from django.shortcuts import render

from orders.models import Order
from carts.models import Cart, CartItem
from datetime import datetime as d
from django.shortcuts import redirect

from carts.models import Cart
from orders.models import Order, DetailOrder
from django.contrib import messages, auth
from store.models import Product


# Create your views here.


def order(request):
    # if request.user.is_authenticated:
    #     cart = Cart.objects.get(user_id=request.user.id)
    #     cart_items = CartItem.objects.filter(
    #         cart=cart)
    # total = 0
    # for cart_item in cart_items:
    #     total += cart_item.product.price * cart_item.quantity
    # order = Order.objects.create(
    #     cart=cart,
    #     create_date=d.now(),
    #     status='New',
    #     total_price= total)
    # order.save()
    # return render(request, 'orders/order_complete.html')
    return render(request, 'orders/payments.html')


def ordered(request):
    cart_items = ''
    cart = ''
    if request.method == "POST":
        number_phone = request.POST.get('phone')
        address = request.POST.get('address')
        result = request.POST.get('result')

    if request.user.is_authenticated:
        cart = Cart.objects.get(user_id=request.user.id)
        cart_items = CartItem.objects.filter(
            cart=cart)
    total = 0
    cart_items_list = [c for c in cart_items]
    for cart_item in cart_items:
        total += (cart_item.product.price - cart_item.product.price*cart_item.product.discount) * cart_item.quantity
        product = Product.objects.get(pk=cart_item.product.id)
        product.quantity -= cart_item.quantity
        product.saled += cart_item.quantity
        product.save()

    total_price = total
    tax = total * 0.1
    total = total + tax
    order = Order.objects.create(
        cart=cart,
        create_date=d.now(),
        status='New',
        total_price=total_price,
        address=address + ' - ' + result,
        number_phone=number_phone
    )
    order.save()

    for cart_item in cart_items:
        # save in detail order
        detailOrder = DetailOrder.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity
        )
        detailOrder.save()

    context = {
        "order": order,
        "cart_items_list": cart_items_list,
        "total_price": total_price,
        "tax": tax,
        "total": total
    }
    cart_items.delete()
    return render(request, 'orders/order_complete.html', context=context)


def list_order(request):
    user = request.user
    # cart
    cart = Cart.objects.get(user=user)
    # order
    ordered = Order.objects.filter(cart=cart)
    context = {
        'ordered': ordered
    }
    return render(request, 'orders/list_order.html', context=context)
