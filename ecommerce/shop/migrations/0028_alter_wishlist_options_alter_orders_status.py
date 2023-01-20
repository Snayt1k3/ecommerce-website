# Generated by Django 4.1.5 on 2023-01-20 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_alter_ordersitem_options_alter_personalarea_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wishlist',
            options={'verbose_name': 'Wish_List', 'verbose_name_plural': 'Wish_Lists'},
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('В сборке у продавца', 'assembl'), ('В доставке', 'delivery'), ('Получен', 'received')], max_length=30),
        ),
    ]
