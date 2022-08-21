from typing import List, Union  # pylint: disable=W0611
from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver  # pylint: disable=W0611
from blog_hillel.apps.users.views import UserListView, UserDetailView

__all__:  List[str] = ["urlpatterns"]

app_name: str = "users"
urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("user/<int:pk>", UserDetailView.as_view(), name="user-detail"),
]
