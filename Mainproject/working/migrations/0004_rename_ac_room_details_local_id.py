# Generated by Django 5.1.4 on 2025-01-13 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('working', '0003_alter_room_details_key_features'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room_details',
            old_name='AC',
            new_name='Local_Id',
        ),
    ]
