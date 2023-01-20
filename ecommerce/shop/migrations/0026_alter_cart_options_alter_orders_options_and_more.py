# Generated by Django 4.1.5 on 2023-01-20 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_remove_orders_products_orders_date_ordersitem_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Cart', 'verbose_name_plural': 'Carts'},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'ordering': ['date'], 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='ordersitem',
            options={'verbose_name': 'OrderItem', 'verbose_name_plural': 'OrderItems'},
        ),
        migrations.AlterModelOptions(
            name='wishlist',
            options={'verbose_name': 'WishList', 'verbose_name_plural': 'WishLists'},
        ),
    ]