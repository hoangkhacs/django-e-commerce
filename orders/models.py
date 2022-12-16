from tkinter.tix import Tree
from django.db import models
from accounts.models import Account
from carts.models import Cart, CartItem
from store.models import Product

# Create your models here.


class Order(models.Model):
    STATUS = (
        ('New', 'Mới'),
        ('Completed', 'Đã thanh toán'),
        ('Cancelled', 'Hủy đơn'),
    )
    cart = models.ForeignKey(
        Cart, on_delete=models.DO_NOTHING, verbose_name=('Giỏ hàng'))
    create_date = models.DateField(verbose_name=('Ngày tạo đơn'))
    status = models.CharField(max_length=200, choices=STATUS,
                              default='New', verbose_name=('Tình trạng đơn hàng'))
    total_price = models.IntegerField(
        editable=False, verbose_name=('Tổng giá'))
    address = models.TextField()
    number_phone = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'

    def getPriceFormatVND(self):
        return '{:3,}'.format(self.total_price)

    def __str__(self):
        return str(self.id)

class DetailOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=("Giỏ hàng"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=("Sản phẩm"))
    quantity = models.IntegerField(verbose_name=("Số lượng"))

    class Meta:
        verbose_name = 'Chi tiết đơn hàng'
        verbose_name_plural = 'Chi tiết đơn hàng'


class Payment(models.Model):
    PAYMENT = (
        ('CASH', "Tiền mặt"),
        ('CARD', 'Thẻ tín dụng')
    )
    user = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING, verbose_name=('Người mua hàng'))
    order = models.OneToOneField(
        Order, on_delete=models.DO_NOTHING, verbose_name=('Đơn hàng'))
    payment_method = models.CharField(
        max_length=200, choices=PAYMENT, default='CASH', verbose_name=('Hình thức thanh toán'))
    create_date = models.DateTimeField(
        auto_now_add=True, verbose_name=('Ngày thanh toán'))

    class Meta:
        verbose_name = 'Thanh toán'
        verbose_name_plural = 'Thanh toán'

    def save(self, *args, **kwargs):
        
        super(Order, self).save(*args, **kwargs)
