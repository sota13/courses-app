# Generated by Django 4.1.2 on 2022-11-15 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0004_remove_instructorskill_detail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructorcontactinfo',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_info', to='instructor.instructor'),
        ),
        migrations.AlterField(
            model_name='instructoreducation',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='education', to='instructor.instructor'),
        ),
        migrations.AlterField(
            model_name='instructorskill',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='instructor.instructor'),
        ),
        migrations.AlterField(
            model_name='instructorsocialmedia',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='social_media', to='instructor.instructor'),
        ),
    ]