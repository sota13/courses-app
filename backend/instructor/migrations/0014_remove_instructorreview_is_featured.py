# Generated by Django 4.1.2 on 2023-02-15 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0013_instructorreview_is_featured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructorreview',
            name='is_featured',
        ),
    ]