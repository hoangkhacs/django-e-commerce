from email.policy import default
from enum import unique
from math import prod
from statistics import quantiles
from tkinter import CASCADE
from tokenize import Triple
from turtle import update

from django.db import models
from django.urls import reverse

from accounts.models import Account
from category.models import Category
from django.utils.safestring import mark_safe


class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=('Tên'))
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = ("Nhà cung cấp")
        verbose_name_plural = ("Nhà cung cấp")

    def __str__(self):
        return self.name


class PublicCompany(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name=('Tên'))
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Nhà xuất bản")
        verbose_name_plural = ("Nhà xuất bản")


class Promotion(models.Model):
    discount = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        verbose_name = ("Khuyến mãi")
        verbose_name_plural = ("Khuyến mãi")


class Author(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            verbose_name=('Tên tác giả'))
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = ("Tác giải")
        verbose_name_plural = ("Tác giả")

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(
        max_length=200, unique=True,  verbose_name=('Tên sách'))
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(
        max_length=2000, blank=True,  verbose_name=('Mô tả'))
    price = models.IntegerField(verbose_name=('Giá '))
    price_import = models.IntegerField(verbose_name=('Giá nhập'))
    quantity = models.IntegerField(default=0,  verbose_name=('Số lượng'))
    saled = models.IntegerField(
        default=0, editable=False,  verbose_name=('Đã bán'))
    size = models.CharField(max_length=20, null=True,
                            verbose_name=('Kích thước'))
    number_page = models.IntegerField(null=True,  verbose_name=('Số trang'))
    is_available = models.BooleanField(
        default=True,  verbose_name=('Trạng thái'))
    # Khi xóa category thì Product bị xóa
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, null=True,  verbose_name=('Thể loại'))
    author = models.ManyToManyField(Author,  verbose_name=('Tác giả'))
    public_company = models.ForeignKey(
        PublicCompany, on_delete=models.CASCADE,  verbose_name=('Nhà xuất bản'))
    public_date = models.DateTimeField(
        auto_now_add=True,  verbose_name=('Ngày phát hành'))
    modified_date = models.DateTimeField(
        auto_now=True,  verbose_name=('Ngày nhập'))
    promotion = models.ForeignKey(
        Promotion, blank=True, null=True, on_delete=models.SET_NULL)
    discount = models.FloatField(default=0)
    likes = models.IntegerField(default=0, editable=False)
    views = models.IntegerField(default=0, editable=False)
    images = models.ImageField(
        upload_to='photos/products',  verbose_name=('Hình ảnh'))

    def image_tag(self):
        return mark_safe('<img src="{}" height="70", width="90px";/>'.format(self.images.url))
    image_tag.short_description = 'Image'

    class Meta:
        verbose_name = ("Sản phẩm")
        verbose_name_plural = ("Sản phẩm")

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def getPriceFormatVND(self):
        return '{:3,}'.format(self.price)
    getPriceFormatVND.short_description = 'Giá'

    def getPriceSaleFormatVND(self):
        return '{:3,}'.format(round(self.price - self.price*self.discount))
    getPriceFormatVND.short_description = 'Giá khuyến mãi'

    def getPriceSaled(self):
        return self.price - self.price*self.discount


class Image(models.Model):
    images = models.ImageField(upload_to='photos/products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Hình ảnh")
        verbose_name_plural = ("Hình ảnh")


class DetailInventory(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=('Sách'))
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, verbose_name=('Nhà cung cấp'))
    amount = models.IntegerField(verbose_name=('Số lượng'))

    class Meta:
        verbose_name = ("Chi tiết phiếu nhập")
        verbose_name_plural = ("Chi tiết phiếu nhập")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_amount = self.amount

    def save(self):
        if not self.pk:
            try:
                result_product = Product.objects.get(id=self.product.id)
                result_product.quantity += self.amount
                result_product.save()
            except:
                pass
        else:
            self.update()
        return super(DetailInventory, self).save()

    def delete(self):
        result_product = Product.objects.get(id=self.product.id)
        result_product.quantity -= self.amount
        result_product.save()
        return super(DetailInventory, self).delete()

    def update(self):
        if self.old_amount != self.amount:
            result_product = Product.objects.get(id=self.product.id)
            result_product.quantity = result_product.quantity - self.old_amount + self.amount
            result_product.save()
        return super(DetailInventory, self).save()


class ReviewRating(models.Model):
    STAR = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=('Sản phẩm'))
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name=('user'))
    ordered = models.BooleanField(default=False, verbose_name=('Đã mua'))
    comment = models.TextField(
        max_length=500, blank=True, verbose_name=('Đánh giá'))
    rating = models.FloatField(choices=STAR, verbose_name=('Sao'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=('Ngày bình luận'))
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Đánh giá sản phẩm")
        verbose_name_plural = ("Đánh giả sản phẩm")

    def save(self, *args, **kwargs):
        if not self.pk:
            from orders.models import Order, DetailOrder
            from carts.models import Cart
            cart = Cart.objects.get(user=self.user)
            orders = Order.objects.filter(cart=cart)
            for order in orders:
                detailOrders = DetailOrder.objects.filter(
                            order=order)
                for detailOrder in detailOrders:
                    if detailOrder.product == self.product:
                        self.ordered = True
        super(ReviewRating, self).save(*args, **kwargs)
