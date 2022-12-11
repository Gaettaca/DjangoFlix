# Generated by Django 4.1.4 on 2022-12-11 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("playlists", "0008_tvshowproxy_tvshowseasonproxy"),
    ]

    operations = [
        migrations.AddField(
            model_name="playlist",
            name="type",
            field=models.CharField(
                choices=[
                    ("MOV", "Movie"),
                    ("TVS", "TV Show"),
                    ("SEA", "Season"),
                    ("PLY", "Playlist"),
                ],
                default="PLY",
                max_length=3,
            ),
        ),
    ]
