# Generated by Django 5.1.4 on 2025-01-14 07:35

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_remove_booking_idproof'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
