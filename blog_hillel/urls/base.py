from typing import List  # pylint: disable=W0611

from django.contrib import admin
from django.urls import path, include, re_path


__all__: List[str] = ["urlpatterns"]

from blog_hillel.apps.articles.views.article import UpdateProfile, RegisterFormView


gettext = lambda string: string  # noqa: E731

# django urls patterns
urlpatterns = [
    path("admin/", admin.site.urls),
]

# blog_hillel urls patterns
urlpatterns += [
    re_path(r"^", include("blog_hillel.apps.articles.urls", namespace="blog_hillel")),
    # re_path(r"^", include("django_api.apps.blog_hillel.urls.api", namespace="blog_hillel")),
]


urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/register/", RegisterFormView.as_view(), name="register"),
    path('accounts/update-profile/', UpdateProfile.as_view(), name='update-profile'),
]
