from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class StreamPlatform(models.Model):
    name = models.CharField(max_length=255)
    about = models.CharField(max_length=255)
    webSite = models.URLField()

    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=255, unique=True)
    storyLine = models.TextField()
    active = models.BooleanField(default=True)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return str(self.rating) + ' | ' + self.watchlist.title
