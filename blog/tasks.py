from celery import shared_task

from django.core.mail import send_mail


@shared_task
def contact_us(subject, message, email):
    send_mail(subject, message, email, ['admin@example.com'])
