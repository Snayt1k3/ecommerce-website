# Generated by Django 4.1.5 on 2023-01-28 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0060_alter_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='WishList',
        ),
    ]