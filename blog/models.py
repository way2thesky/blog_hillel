from django.conf import settings
from django.db import models
from django.utils import timezone


class Blog(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=250, unique_for_date='publish')

    image = models.ImageField(upload_to='featured_image/%Y/%m/%d/', blank=True, null=True)  # noqa DJ01

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_description = models.TextField(blank=True)

    posted = models.BooleanField(default=False)
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-posted']

    def __str__(self):
        return self.title

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

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_comments(self):
        return BlogComment.objects.filter(parent=self).filter(active=True)
