# Generated by Django 5.2 on 2025-04-11 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0008_alter_attendance_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='remarks',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
