# Generated by Django 4.1.2 on 2023-03-15 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0017_alter_listingrequest_request_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='listing_status',
            field=models.CharField(choices=[('listed', 'listed'), ('unlisted', 'unlisted'), ('pending', 'pending')], default='unlisted', max_length=20, verbose_name='Status of Listing'),
        ),
    ]
