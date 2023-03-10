# Generated by Django 4.1.5 on 2023-01-23 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0037_personalarea_your_products_product_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_cart', models.IntegerField()),
                ('remove_cart', models.IntegerField()),
                ('add_wish_list', models.IntegerField()),
                ('remove_wish_list', models.IntegerField()),
                ('bought', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
