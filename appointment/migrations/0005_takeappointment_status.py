# Generated by Django 4.0.2 on 2022-04-15 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_remove_takeappointment_status_appointment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='takeappointment',
            name='status',
            field=models.TextField(default='PENDING'),
        ),
    ]
