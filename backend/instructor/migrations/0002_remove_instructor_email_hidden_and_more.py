# Generated by Django 4.1.2 on 2022-11-09 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='email_hidden',
        ),
        migrations.RemoveField(
            model_name='instructor',
            name='phone_number_hidden',
        ),
        migrations.CreateModel(
            name='InstructorSocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='instructor.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='InstructorSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('detail', models.CharField(blank=True, max_length=100, null=True)),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='instructor.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='InstructorEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(blank=True, max_length=100, null=True)),
                ('detail', models.CharField(blank=True, max_length=100, null=True)),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='instructor.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='InstructorContactInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('detail', models.CharField(blank=True, max_length=100, null=True)),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='instructor.instructor')),
            ],
        ),
    ]