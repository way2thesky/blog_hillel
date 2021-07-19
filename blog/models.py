from django.db import models
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=300)
    full_description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    username= models.CharField(max_length=100)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
