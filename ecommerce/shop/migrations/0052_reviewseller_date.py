# Generated by Django 4.1.5 on 2023-01-27 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0051_personalarea_avg_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewseller',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
