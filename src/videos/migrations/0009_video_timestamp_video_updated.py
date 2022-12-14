# Generated by Django 4.1.4 on 2022-12-08 20:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("videos", "0008_rename_timestamp_video_publish_timestamp"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="timestamp",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="video",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
