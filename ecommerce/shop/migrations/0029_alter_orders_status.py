# Generated by Django 4.1.5 on 2023-01-20 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_alter_wishlist_options_alter_orders_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('В сборке у продавца', 'assembl'), ('В доставке', 'delivery'), ('Получен', 'received')], default='В сборке у продавца', max_length=30),
        ),
    ]
