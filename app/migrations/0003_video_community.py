# Generated by Django 2.2 on 2021-06-13 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210613_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='app.Community'),
        ),
    ]
