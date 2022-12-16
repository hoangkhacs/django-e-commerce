from django.db import models
from store.models import Product
from accounts.models import Account

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, blank=True, null=True, verbose_name=('user'))
    cart_id = models.CharField(max_length=250, blank=True, verbose_name=('Mã giỏ hàng'))
    date_create = models.DateTimeField(auto_now_add=True, verbose_name=('Ngày tạo'))

    class Meta:
        verbose_name = ("Giỏ hàng")
        verbose_name_plural = ("Giỏ hàng")
    
    def __str__(self):
        return self.user.email


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=("Giỏ hàng"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=("Sản phẩm"))
    quantity = models.IntegerField(verbose_name=("Số lượng"))

    class Meta:
        verbose_name = ("Chi tiết giỏ hàng")
        verbose_name_plural = ("Chi tiết giỏ hàng")

    def __str__(self):
        return self.product.product_name
