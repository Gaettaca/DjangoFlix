# Generated by Django 4.1.4 on 2022-12-10 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("videos", "0010_alter_video_video_id"),
        ("playlists", "0003_playlist_videos"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playlist",
            name="video",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="videos.video",
            ),
        ),
    ]
