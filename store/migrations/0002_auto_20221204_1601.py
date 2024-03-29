# Generated by Django 3.2 on 2022-12-04 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Tác giải', 'verbose_name_plural': 'Tác giả'},
        ),
        migrations.AlterModelOptions(
            name='detailinventory',
            options={'verbose_name': 'Chi tiết giỏ hàng', 'verbose_name_plural': 'Chi tiết giỏ hàng'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Hình ảnh', 'verbose_name_plural': 'Hình ảnh'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Sản phẩm', 'verbose_name_plural': 'Sản phẩm'},
        ),
        migrations.AlterModelOptions(
            name='promotion',
            options={'verbose_name': 'Khuyến mãi', 'verbose_name_plural': 'Khuyến mãi'},
        ),
        migrations.AlterModelOptions(
            name='publiccompany',
            options={'verbose_name': 'Nhà xuất bản', 'verbose_name_plural': 'Nhà xuất bản'},
        ),
        migrations.AlterModelOptions(
            name='reviewrating',
            options={'verbose_name': 'Đánh giá sản phẩm', 'verbose_name_plural': 'Đánh giả sản phẩm'},
        ),
        migrations.AlterModelOptions(
            name='supplier',
            options={'verbose_name': 'Nhà cung cấp', 'verbose_name_plural': 'Nhà cung cấp'},
        ),
        migrations.AddField(
            model_name='reviewrating',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Tên'),
        ),
    ]
