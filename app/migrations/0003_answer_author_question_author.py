# Generated by Django 5.1.2 on 2024-11-03 15:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_title_tag_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.profile'),
        ),
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.profile'),
        ),
    ]