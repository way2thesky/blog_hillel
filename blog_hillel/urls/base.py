from typing import List  # pylint: disable=W0611

from django.contrib import admin
from django.urls import path, include, re_path

from blog_hillel.apps.articles.views.article import UpdateProfile, RegisterFormView, index

__all__: List[str] = ["urlpatterns"]


gettext = lambda string: string  # noqa: E731

# django urls patterns
urlpatterns = [
    path("admin/", admin.site.urls),
]

# blog_hillel urls patterns
urlpatterns += [
    re_path(r"^$", index, name="index"),
    re_path(r"articles/", include("blog_hillel.apps.articles.urls", namespace="articles")),
    re_path(r"users/", include("blog_hillel.apps.users.urls", namespace="users")),
]

urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", RegisterFormView.as_view(), name="register"),
    path("accounts/update-profile/", UpdateProfile.as_view(), name="update-profile"),
]
