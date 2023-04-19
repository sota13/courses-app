# Generated by Django 4.1.2 on 2022-11-09 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userprofile_first_name_userprofile_is_instructor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, default="I'm good at teaching many courses for example I teach...", max_length=3000, null=True),
        ),
    ]
