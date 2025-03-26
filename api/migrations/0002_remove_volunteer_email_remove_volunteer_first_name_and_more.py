# Generated by Django 4.2.17 on 2025-02-15 01:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='volunteers', to=settings.AUTH_USER_MODEL),
        ),
    ]
