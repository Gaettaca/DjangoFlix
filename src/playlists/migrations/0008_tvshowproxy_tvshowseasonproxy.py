# Generated by Django 4.1.4 on 2022-12-11 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("playlists", "0007_playlist_order_playlist_parent"),
    ]

    operations = [
        migrations.CreateModel(
            name="TVShowProxy",
            fields=[],
            options={
                "verbose_name": "TV Show",
                "verbose_name_plural": "TV Shows",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("playlists.playlist",),
        ),
        migrations.CreateModel(
            name="TVShowSeasonProxy",
            fields=[],
            options={
                "verbose_name": "Season",
                "verbose_name_plural": "Seasons",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("playlists.playlist",),
        ),
    ]