# Generated by Django 4.1.5 on 2023-01-26 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0044_alter_personalarea_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalarea',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
