# Generated by Django 4.1.5 on 2023-01-19 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_remove_orders_product_orders_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]