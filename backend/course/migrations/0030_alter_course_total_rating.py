# Generated by Django 4.1.2 on 2023-01-14 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0029_course_total_rating_delete_soldcourse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='total_rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
