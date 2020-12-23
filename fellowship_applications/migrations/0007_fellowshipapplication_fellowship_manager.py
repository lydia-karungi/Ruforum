# Generated by Django 2.2.2 on 2020-12-16 07:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fellowship_applications', '0006_auto_20201214_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='fellowshipapplication',
            name='fellowship_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fellowship_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
