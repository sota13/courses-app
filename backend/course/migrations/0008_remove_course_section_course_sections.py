# Generated by Django 4.1.2 on 2022-11-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_course_discount_enabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='section',
        ),
        migrations.AddField(
            model_name='course',
            name='sections',
            field=models.ManyToManyField(related_name='courses', to='course.section'),
        ),
    ]
