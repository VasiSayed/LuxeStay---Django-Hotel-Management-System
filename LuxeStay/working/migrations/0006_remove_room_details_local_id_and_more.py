# Generated by Django 5.1.4 on 2025-01-18 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('working', '0005_room_details_disable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room_details',
            name='Local_Id',
        ),
        migrations.RemoveField(
            model_name='room_details',
            name='avalibilty',
        ),
        migrations.AddField(
            model_name='room_details',
            name='max_guest',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
