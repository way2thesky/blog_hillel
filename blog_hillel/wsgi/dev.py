# blog_hillel/wsgi/dev.py


import os
from typing import List  # pylint: disable=W0611

from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application


__all__: List[str] = ["application"]


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_hillel.settings.dev")
application: WSGIHandler = get_wsgi_application()
