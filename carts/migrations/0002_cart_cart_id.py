# Generated by Django 3.2 on 2022-10-29 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]