# Generated by Django 3.2 on 2022-12-13 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20221212_2018'),
        ('orders', '0004_alter_order_number_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Số lượng')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Đơn hàng')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Sản phẩm')),
            ],
            options={
                'verbose_name': 'Chi tiết đơn hàng',
                'verbose_name_plural': 'Chi tiết đơn hàng',
            },
        ),
    ]
