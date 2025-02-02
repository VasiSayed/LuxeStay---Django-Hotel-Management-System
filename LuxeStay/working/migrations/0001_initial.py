# Generated by Django 5.1.4 on 2025-01-12 08:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh', 'Arunachal Pradesh'), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chhattisgarh', 'Chhattisgarh'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal'), ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'), ('Chandigarh', 'Chandigarh'), ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'), ('Delhi', 'Delhi'), ('Jammu and Kashmir', 'Jammu and Kashmir'), ('Ladakh', 'Ladakh'), ('Lakshadweep', 'Lakshadweep'), ('Puducherry', 'Puducherry')], max_length=50, unique=True)),
                ('Image', models.ImageField(upload_to='media/images/')),
                ('City_name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Residency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('logo', models.ImageField(upload_to='images/residency/logo')),
                ('area', models.CharField(default='', max_length=50)),
                ('city', models.CharField(default='', max_length=50)),
                ('state', models.CharField(choices=[('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh', 'Arunachal Pradesh'), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chhattisgarh', 'Chhattisgarh'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal'), ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'), ('Chandigarh', 'Chandigarh'), ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'), ('Delhi', 'Delhi'), ('Jammu and Kashmir', 'Jammu and Kashmir'), ('Ladakh', 'Ladakh'), ('Lakshadweep', 'Lakshadweep'), ('Puducherry', 'Puducherry')], default='Maharashtra', max_length=50)),
                ('country', models.CharField(default='', max_length=50)),
                ('manage_name', models.CharField(max_length=40)),
                ('contact_no', models.CharField(max_length=10)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'area')},
            },
        ),
        migrations.CreateModel(
            name='Room_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(choices=[('Economy', 'Economy'), ('Standard', 'Standard'), ('Deluxe', 'Deluxe'), ('Super Deluxe', 'Super Deluxe'), ('Suite', 'Suite'), ('Junior Suite', 'Junior Suite'), ('Presidential Suite', 'Presidential Suite'), ('Family Room', 'Family Room'), ('Studio', 'Studio'), ('Penthouse', 'Penthouse')], default='Queen', max_length=30)),
                ('bed_type', models.CharField(choices=[('King', 'King'), ('Queen', 'Queen'), ('Twin', 'Twin'), ('Single', 'Single')], default='Queen', max_length=20)),
                ('residency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='working.residency')),
            ],
            options={
                'unique_together': {('residency', 'type_name', 'bed_type')},
            },
        ),
        migrations.CreateModel(
            name='Room_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.CharField(max_length=10)),
                ('picture', models.ImageField(upload_to='images/residency/roomimages')),
                ('key_features', models.JSONField(blank=True, default=dict, null=True)),
                ('AC', models.BooleanField(default=True)),
                ('avalibilty', models.BooleanField(default=True)),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
                ('residency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='working.residency')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='working.room_type')),
            ],
            options={
                'unique_together': {('residency', 'room_no')},
            },
        ),
    ]
