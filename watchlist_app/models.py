from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.title
