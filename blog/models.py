from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Blog(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=250, unique_for_date='publish')

    image = models.ImageField(blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_description = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5)
    posted = models.BooleanField(default=False)
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()
    ags = TaggableManager()

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

    def get_absolute_url(self):
        return reverse('blog:post-detail', args=[str(self.id)])


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")

    text = models.TextField()
    active = models.BooleanField(default=False)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
