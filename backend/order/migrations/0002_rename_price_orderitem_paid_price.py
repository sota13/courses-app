# Generated by Django 4.1.2 on 2023-01-08 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='price',
            new_name='paid_price',
        ),
    ]