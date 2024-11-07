# Generated by Django 5.1.2 on 2024-11-07 17:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]