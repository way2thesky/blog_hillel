from typing import List

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


__all__: List[str] = ["ArticlesConfig"]


class ArticlesConfig(AppConfig):
    """Application config."""

    name: str = "blog_hillel.apps.articles"
    verbose_name: str = _("Articles")
