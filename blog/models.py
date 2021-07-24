from django.db import models
from django.conf import settings
from datetime import date

from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Blog(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')

    image = models.ImageField(upload_to='featured_image/%Y/%m/%d/', blank=True, null=True)  # this

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_description = models.TextField(blank=True)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    # to get comment with parent is none and active is true, we can use this in template
    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)


class BlogComment(models.Model):
    username = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here.")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)

    class Meta:
        ordering = ('-post_date',)

    def __str__(self):
        return self.username

    def get_comments(self):
        return BlogComment.objects.filter(parent=self).filter(active=True)