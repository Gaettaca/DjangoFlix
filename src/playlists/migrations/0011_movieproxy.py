# Generated by Django 4.1.4 on 2022-12-11 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("playlists", "0010_alter_playlist_parent"),
    ]

    operations = [
        migrations.CreateModel(
            name="MovieProxy",
            fields=[],
            options={
                "verbose_name": "Movie",
                "verbose_name_plural": "Movies",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("playlists.playlist",),
        ),
    ]
