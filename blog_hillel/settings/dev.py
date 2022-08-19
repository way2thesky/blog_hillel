# blog_hillel/settings/dev.py

from blog_hillel.settings.base import *  # noqa: F401, F403


DEBUG: bool = True

WSGI_APPLICATION: str = "blog_hillel.wsgi.dev.application"
ASGI_APPLICATION: str = "blog_hillel.asgi.dev.application"

ROOT_URLCONF: str = "blog_hillel.urls.dev"

# security settings
SESSION_COOKIE_SECURE: bool = False  # noqa: F405
CSRF_COOKIE_SECURE: bool = False  # noqa: F405
