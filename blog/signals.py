from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Blog, BlogComment


@receiver(post_save, sender=Blog)
def post_post_save(sender, instance, **kwargs):
    if kwargs['created']:  # true if the instance is created
        subject = 'New post'
        message = f'New post "{instance.title}" created! Check it on admin panel.'
        from_email = 'ad@ex.com'
        send_mail(subject, message, from_email, ['admin@example.com'])


@receiver(post_save, sender=BlogComment)
def comment_post_save(sender, instance, **kwargs):
    if kwargs['created']:  # true if the instance is created
        subject = 'New comment'
        message = 'New comment created! Check it on admin panel.'
        from_email = 'ad@ex.com'
        send_mail(subject, message, from_email, ['admin@example.com'])


@receiver(post_save, sender=BlogComment)
def comment_author_post_save(sender, instance, **kwargs):
    if kwargs['created']:  # true if the instance is created
        subject = 'New comment on your post'
        message = f'New comment created! You can check it here http://127.0.0.1:8000/blog/post/{instance.post.pk}'
        from_email = 'ad@ex.com'
        send_mail(subject, message, from_email, [instance.post.user.email])
