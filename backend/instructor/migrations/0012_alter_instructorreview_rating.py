# Generated by Django 4.1.2 on 2023-02-14 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0011_instructorrequest_decision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructorreview',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
