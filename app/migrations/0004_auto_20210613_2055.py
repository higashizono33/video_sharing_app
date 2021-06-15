# Generated by Django 2.2 on 2021-06-13 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_video_community'),
    ]

    operations = [
        migrations.AddField(
            model_name='videogroup',
            name='community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_groups', to='app.Community'),
        ),
        migrations.AlterField(
            model_name='video',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='app.VideoGroup'),
        ),
    ]