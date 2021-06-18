# Generated by Django 3.2.4 on 2021-06-18 06:29

import analyticsApi.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analyticsApi', '0003_rename_is_banker_user_is_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activation',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='analyticsApi.user')),
                ('passport_photo', models.ImageField(upload_to=analyticsApi.models.upload_image)),
                ('identification_number', models.IntegerField()),
                ('identification_doc', models.ImageField(upload_to=analyticsApi.models.upload_image)),
                ('driving_license_picture', models.ImageField(blank=True, upload_to=analyticsApi.models.upload_image)),
                ('residence', models.CharField(max_length=255)),
                ('KRA_pin', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_valid',
            field=models.BooleanField(default=False),
        ),
    ]