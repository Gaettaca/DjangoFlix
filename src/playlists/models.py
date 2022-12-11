from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

from djangoflix.db.models import PublishStateOptions
from djangoflix.db.receivers import publish_state_pre_save, slugify_pre_save

from categories.models import Category
from videos.models import Video


class PublishStateOptions(models.TextChoices):
    # CONSTANT = DB_VALUE, USER_DISPLAY_VA
    PUBLISH = 'PU', 'Published'
    DRAFT = 'DR', 'Draft'
    # UNLISTED = 'UN', 'Unlisted'
    # PRIVATE = 'PR', 'Private'


# to simplify data filtering
class PlaylistQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return Playlist.objects.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now)


class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Playlist(models.Model):
    class PlaylistTypeCoices(models.TextChoices):
        MOVIE = "MOV", "Movie"
        SHOW = "TVS", "TV Show"
        SEASON = "SEA", "Season"
        PLAYLIST = "PLY", "Playlist"

    category = models.ForeignKey(Category, blank=True, null=True,
                                 related_name='playlists', on_delete=models.SET_NULL)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    order = models.IntegerField(default=1)

    video = models.ForeignKey(Video, blank=True, null=True, related_name='playlist_featured',
                              on_delete=models.SET_NULL)  # one video per list

    videos = models.ManyToManyField(Video, related_name='playlist_item', blank=True,
                                    through='PlaylistItem')

    type = models.CharField(max_length=3, choices=PlaylistTypeCoices.choices,
                            default=PlaylistTypeCoices.PLAYLIST)
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices,
                             default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False,
                                             blank=True, null=True)
    objects = PlaylistManager()

    @property
    def is_published(self):
        return self.active

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


pre_save.connect(publish_state_pre_save, sender=Playlist)
pre_save.connect(slugify_pre_save, sender=Playlist)


class TVShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True,
                                          type=Playlist.PlaylistTypeCoices.SHOW)


class TVShowProxy(Playlist):
    objects = TVShowProxyManager()

    class Meta:
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeCoices.SHOW
        super().save(*args, **kwargs)


class MovieProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(type=Playlist.PlaylistTypeCoices.MOVIE)


class MovieProxy(Playlist):
    objects = MovieProxyManager()

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeCoices.MOVIE
        super().save(*args, **kwargs)


class TVShowSeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False,
                                          type=Playlist.PlaylistTypeCoices.SEASON)


class TVShowSeasonProxy(Playlist):
    objects = TVShowSeasonProxyManager()

    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeCoices.SEASON
        super().save(*args, **kwargs)


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-timestamp']
