# Generated by Django 4.1.2 on 2023-02-02 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0010_instructor_approved_date_instructor_request_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructorrequest',
            name='decision',
            field=models.CharField(blank=True, choices=[('approved', 'approved'), ('rejected', 'rejected')], max_length=20, null=True),
        ),
    ]
