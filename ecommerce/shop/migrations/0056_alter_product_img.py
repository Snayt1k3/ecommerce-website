# Generated by Django 4.1.5 on 2023-01-28 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0055_alter_reviewseller_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(upload_to='products'),
        ),
    ]