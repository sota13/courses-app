# Generated by Django 4.1.2 on 2022-11-15 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_remove_course_skills_course_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='short_description',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
