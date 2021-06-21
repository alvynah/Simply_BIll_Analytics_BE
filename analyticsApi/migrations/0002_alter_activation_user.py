# Generated by Django 3.2.4 on 2021-06-21 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analyticsApi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activation',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='activation', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]