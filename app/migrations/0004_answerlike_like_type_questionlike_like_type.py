# Generated by Django 5.1.2 on 2024-12-15 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_image_name_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='answerlike',
            name='like_type',
            field=models.CharField(choices=[('like', 'Like'), ('dislike', 'Dislike')], default='like', max_length=7),
        ),
        migrations.AddField(
            model_name='questionlike',
            name='like_type',
            field=models.CharField(choices=[('like', 'Like'), ('dislike', 'Dislike')], default='like', max_length=7),
        ),
    ]
