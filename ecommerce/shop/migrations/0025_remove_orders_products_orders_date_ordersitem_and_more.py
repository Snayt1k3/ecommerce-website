# Generated by Django 4.1.5 on 2023-01-20 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_rename_city_personalarea_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='products',
        ),
        migrations.AddField(
            model_name='orders',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.CreateModel(
            name='OrdersItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='order_items',
            field=models.ManyToManyField(to='shop.ordersitem'),
        ),
    ]
