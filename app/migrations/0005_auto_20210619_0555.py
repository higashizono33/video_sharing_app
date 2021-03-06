# Generated by Django 2.2 on 2021-06-19 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_auto_20210613_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='posted_by',
        ),
        migrations.AddField(
            model_name='post',
            name='resident_posted',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='app.Resident'),
        ),
        migrations.AddField(
            model_name='post',
            name='user_posted',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
