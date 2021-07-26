from django.db import models
from django.conf import settings
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
    title = models.CharField(max_length=200)
    short_description = models.SlugField(max_length=250, unique_for_date='publish')

    image = models.ImageField(upload_to='featured_image/%Y/%m/%d/', blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_description = models.TextField(blank=True)

    posted = models.BooleanField(default=False)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    objects = models.Manager()  # The default manager.
    published = PublishedManager()

    tags = TaggableManager()

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)


class BlogComment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")

    text = models.TextField()
    active = models.BooleanField(default=False)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name

    def get_comments(self):
        return BlogComment.objects.filter(parent=self).filter(active=True)
