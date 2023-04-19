# Generated by Django 4.1.2 on 2022-12-24 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0025_publicationrequest_terms_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='num_reviews',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
