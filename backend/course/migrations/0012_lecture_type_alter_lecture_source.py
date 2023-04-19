# Generated by Django 4.1.2 on 2022-12-06 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_coursefaq_coursebenefit'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='type',
            field=models.CharField(choices=[('premium', 'paid lecture'), ('free', 'free lecture')], default='premium', max_length=20, verbose_name='Type of Lecture'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='source',
            field=models.FileField(null=True, upload_to='new-lectures/'),
        ),
    ]