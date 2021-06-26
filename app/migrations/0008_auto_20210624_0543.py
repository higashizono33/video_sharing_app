# Generated by Django 2.2 on 2021-06-24 10:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_video_user_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='user_like',
            field=models.ManyToManyField(related_name='video_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
