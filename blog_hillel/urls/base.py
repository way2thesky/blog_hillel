from typing import List  # pylint: disable=W0611

from django.contrib import admin
from django.urls import path, include, re_path


__all__: List[str] = ["urlpatterns"]

gettext = lambda string: string  # noqa: E731

# django urls patterns
urlpatterns = [
    path("admin/", admin.site.urls),
]

# blog_hillel urls patterns
# urlpatterns += [
#     re_path(r"^", include("django_api.apps.users.urls.api", namespace="users")),
#     re_path(r"^", include("django_api.apps.blog_hillel.urls.api", namespace="blog_hillel")),
# ]
