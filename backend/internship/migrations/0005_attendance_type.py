# Generated by Django 5.2 on 2025-04-10 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0004_remove_attendance_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='type',
            field=models.CharField(default='f2f', max_length=255),
        ),
    ]
