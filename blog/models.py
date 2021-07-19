from django.db import models
from django.conf import settings
from datetime import date
from django.utils import timezone


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=300)
    full_description = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    posted = models.BooleanField(default=False)
    post_date = models.DateField(default=date.today)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    username = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here.")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)

    def __str__(self):
        return self.username
