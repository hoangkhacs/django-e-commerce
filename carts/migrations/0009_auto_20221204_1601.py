# Generated by Django 3.2 on 2022-12-04 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20221204_1601'),
        ('carts', '0008_rename_quanlity_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Giỏ hàng', 'verbose_name_plural': 'Giỏ hàng'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Sản phẩm giỏ hàng', 'verbose_name_plural': 'Sản phẩm giỏ hàng'},
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.cart', verbose_name='Giỏ hàng'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Sản phẩm'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(verbose_name='Số lượng'),
        ),
    ]