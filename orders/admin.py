from django.contrib import admin
from django.db import models
from .models import Order, Payment, DetailOrder

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'create_date', 'status', 'total_price')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'payment_method', 'create_date')


class DetailOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')


admin.site.register(Order, OrderAdmin)
# admin.site.register(Payment, PaymentAdmin)
admin.site.register(DetailOrder, DetailOrderAdmin)
