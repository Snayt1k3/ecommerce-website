# Generated by Django 4.1.5 on 2023-01-20 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_alter_orders_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalarea',
            name='avatar',
            field=models.ImageField(upload_to='media/avatars/'),
        ),
    ]
