from re import split
from carts.models import Cart, CartItem
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Sum, F, FloatField
from django.db.models.functions import ExtractMonth, ExtractDay
from django.db.models import Count
from django.db.models import IntegerField


from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account
from django.core.mail import EmailMessage
import datetime
from store.models import Product
from orders.models import Order
from category.models import Category


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password,  phone_number=phone_number)
            user.save()
            messages.success(
                request=request,
                message="Đăng ký thành công!"
            )
            return redirect('login')

        else:
            messages.error(request=request, message="Đăng ký thất bại!")
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context=context)


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart)
            except Exception:
                pass
            auth.login(request=request, user=user)
            # if (user.is_superuser == True):
            #     return redirect('home')
            messages.success(request=request, message="Đăng nhập thành công!")
            return redirect('home')

        else:
            messages.error(request=request,
                           message="Email hoặc mật khẩu không chính xác!")
    context = {
        'email': email if 'email' in locals() else '',
        'password': password if 'password' in locals() else '',
    }
    return render(request, 'accounts/login.html', context=context)


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    # messages.success(request=request, message="You are logged out!")
    return redirect('home')


def dashboard(request):
    users = Account.objects.all().order_by("-last_login")
    products = Product.objects.all()
    orders = Order.objects.all()
    time_now = datetime.datetime.now().time()
    output = (
        Order.objects.filter(status="Completed")
        .annotate(
            month=ExtractMonth("create_date")
        )
        .values("month")
        .annotate(
            total=Sum(
                F("total_price"),
                output_field=IntegerField()
            )
        )
        .order_by("month")
    )

    output_day = (
        Order.objects.filter(status="Completed")
        .annotate(
            day=ExtractDay("create_date")
        )
        .values("day")
        .annotate(
            total=Sum(
                F("total_price"),
                output_field=IntegerField()
            )
        )
        .order_by("day")
    )
    output_saled = (
        Product.objects.filter(is_available=True)
        .values("product_name", "saled")
        .order_by("-saled")
    )

    output_quantity = (
        Product.objects.filter(is_available=True)
        .values("product_name", "quantity")
        .order_by("-quantity")
    )
    context = {
        'users': users,
        'count_user': users.count(),
        'count_product': products.count(),
        'count_order': orders.count(),
        'time_now': time_now,
        'output': output,
        'output_day': output_day,
        'output_saled': output_saled[:5],
        "output_quantity": output_quantity[:5]
    }
    return render(request, "accounts/dashboard.html", context=context)
