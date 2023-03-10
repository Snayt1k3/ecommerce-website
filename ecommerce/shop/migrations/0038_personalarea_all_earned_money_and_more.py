# Generated by Django 4.1.5 on 2023-01-24 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0037_personalarea_your_products_product_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalarea',
            name='all_earned_money',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='personalarea',
            name='all_spent_money',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
