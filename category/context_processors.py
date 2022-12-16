from .models import Category
from carts.models import CartItem, Cart
from django.shortcuts import get_object_or_404


def extras(request):
    nodes = Category.objects.all()
    return dict(nodes=nodes)

def count_cart(request):
    count_cart = ''
    if request.user.is_authenticated:
        # cart = get_object_or_404(Cart, user_id = request.user.id)
        try:
            cart = Cart.objects.get(user_id = request.user.id)
            count_cart = CartItem.objects.filter(cart=cart)
        except:
            pass
    return dict(count_cart=len(count_cart))