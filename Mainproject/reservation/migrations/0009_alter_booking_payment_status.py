# Generated by Django 5.1.4 on 2025-01-22 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0008_booking_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(choices=[('Successfull', 'Successfull'), ('Fail', 'Fail'), ('Pending', 'Pending')], default='Pending', max_length=20),
        ),
    ]
