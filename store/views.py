import django
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse



from carts.models import Cart, CartItem
from carts.views import _cart_id
from category.models import Category
from store.filters import ProductFilter
from store.models import Author, Product, PublicCompany, Supplier, ReviewRating
from carts.models import Cart, CartItem

# Create your views here.


def store(request, category_slug=None):
    category_name = ''
    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        category_name = category.category_name
        categories = Category.objects.get(
            id=category.id).get_descendants(include_self=True)

        products = Product.objects.filter(category__in=categories)

        images = Product.objects.values_list("images", flat=True)

        if 'price' in request.GET:
            price_range = str(request.GET.get('price'))
            price_range = price_range.split(",")
            price_min = price_range[0]
            price_max = price_range[1]
            products = products.filter(price__range=(
                price_min, price_max), is_available=True)
        if 'public_company' in request.GET:
            products = products.filter(
                Q(public_company__name__in=request.GET.getlist('public_company')), is_available=True)
        if 'author' in request.GET:
            products = products.filter(
                Q(author__name__in=request.GET.getlist('author')), is_available=True)
        if 'sort' in request.GET:
            if request.GET.get('sort') == 'l2h':
                products = products.order_by('price')
            elif request.GET.get('sort') == 'h2l':
                products = products.order_by('-price')

    else:
        products = Product.objects.all().filter(is_available=True)
        if 'price' in request.GET:
            price_range = str(request.GET.get('price'))
            price_range = price_range.split(",")
            price_min = price_range[0]
            price_max = price_range[1]
            products = Product.objects.filter(price__range=(
                price_min, price_max), is_available=True)
        if 'public_company' in request.GET:
            products = products.filter(
                Q(public_company__name__in=request.GET.getlist('public_company')), is_available=True)
        if 'author' in request.GET:
            products = products.filter(
                Q(author__name__in=request.GET.getlist('author')), is_available=True)
        if 'sort' in request.GET:
            if request.GET.get('sort') == 'l2h':
                products = products.order_by('price')
            elif request.GET.get('sort') == 'h2l':
                products = products.order_by('-price')

    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 9)
    paged_products = paginator.get_page(page)
    products_count = products.count()
    public_company = PublicCompany.objects.all()
    authors = Author.objects.all()

    context = {
        'products': paged_products,
        'product_count': products_count,
        'public_company': public_company,
        'authors': authors,
        'category_name': category_name
    }
    return render(request, 'store/store.html', context=context)


def product_detail(request, category_slug, product_slug=None):
    product = Product.objects.get(
        category__slug=category_slug, slug=product_slug)
    author = Author.objects.filter(product=product)
    product_relate = Product.objects.filter(category__slug=category_slug)
    comments = ReviewRating.objects.filter(product=product)

    category = get_object_or_404(Category, slug=category_slug)
    # category = Category.objects._mptt_filter(slug=category_slug)
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user_id=request.user.id)
            cart_items = CartItem.objects.filter(
                cart=cart)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
            cart_items = CartItem.objects.filter(cart=cart)
    except ObjectDoesNotExist:
        pass    # Chỉ bỏ qua
    reviews_count = comments.count()
    context = {
        'product': product,
        'author': author,
        'product_relate': product_relate,
        'category': category,
        'reviews': comments,
        'reviews_count': reviews_count
    }
    return render(request, 'store/product_detail.html', context=context)


def search(request):
    if 'q' in request.GET:
        q = request.GET.get('q')
        if q == '':
            return redirect('store')
        else:
            products = Product.objects.filter(
                Q(product_name__icontains=q) | Q(description__icontains=q))
            product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        q = ''
        if 'price' in request.GET:
            price_range = str(request.GET.get('price'))
            price_range = price_range.split(",")
            price_min = price_range[0]
            price_max = price_range[1]
            products = products.filter(price__range=(
                price_min, price_max), is_available=True)
        if 'public_company' in request.GET:
            products = products.filter(
                Q(public_company__name__in=request.GET.getlist('public_company')), is_available=True)
        if 'author' in request.GET:
            products = products.filter(
                Q(author__name__in=request.GET.getlist('author')), is_available=True)

    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 9)
    paged_products = paginator.get_page(page)
    products_count = products.count()
    public_company = PublicCompany.objects.all()
    authors = Author.objects.all()
    context = {
        'products': products,
        'q': q,
        'product_count': products_count,
        'public_company': public_company,
        'authors': authors,
    }
    return render(request, 'store/store.html', context=context)


def add_rating(request, product_id):
    url = request.META.get('HTTP_REFERER')
    user_id=request.user.id
    review = ''
    if request.method == 'POST':
        if 'rating' in request.POST:
            rating = request.POST.get('rating')
        if 'review' in request.POST:
            review = request.POST.get('review')
    commented = ReviewRating.objects.create(
        product_id = product_id,
        user_id = user_id,
        comment = review,
        rating = rating
    )
    commented.save()
    return redirect(url)
    

