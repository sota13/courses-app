# Generated by Django 4.1.2 on 2022-12-12 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0018_lecture_convert_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='duration',
            field=models.FloatField(default=0),
        ),
    ]
