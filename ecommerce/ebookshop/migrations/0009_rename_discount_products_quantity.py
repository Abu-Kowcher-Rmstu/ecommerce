# Generated by Django 4.0.1 on 2022-03-21 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebookshop', '0008_alter_products_author_alter_products_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='discount',
            new_name='quantity',
        ),
    ]
