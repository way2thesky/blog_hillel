from typing import List

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


__all__: List[str] = ["UsersConfig"]


class UsersConfig(AppConfig):
    """Application config."""

    name: str = "blog_hillel.apps.users"
    verbose_name: str = _("Users")
