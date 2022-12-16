# Generated by Django 3.2 on 2022-12-07 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '0009_auto_20221204_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, max_length=250, verbose_name='Mã giỏ hàng'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]