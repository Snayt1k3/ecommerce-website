# Generated by Django 4.1.5 on 2023-01-11 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_rename_product_review_pr_slug_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='pr_slug',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='reviewimages',
            old_name='pr_slug',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='reviewimages',
            old_name='review_id',
            new_name='review',
        ),
    ]
