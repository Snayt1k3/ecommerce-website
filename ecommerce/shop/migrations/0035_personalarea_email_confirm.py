# Generated by Django 4.1.5 on 2023-01-21 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0034_alter_personalarea_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalarea',
            name='email_confirm',
            field=models.BooleanField(default=False),
        ),
    ]
