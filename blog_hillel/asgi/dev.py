# blog_hillel/asgi/dev.py


import os
from typing import List  # pylint: disable=W0611

from django.core.asgi import get_asgi_application


__all__: List[str] = ["application"]


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_hillel.settings.dev")
application = get_asgi_application()
