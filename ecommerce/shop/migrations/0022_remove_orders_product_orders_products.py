# Generated by Django 4.1.5 on 2023-01-19 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_remove_orders_ordersitem_orders_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='product',
        ),
        migrations.AddField(
            model_name='orders',
            name='products',
            field=models.ManyToManyField(to='shop.product'),
        ),
    ]