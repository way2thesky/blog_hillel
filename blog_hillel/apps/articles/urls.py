from django.urls import path

from blog_hillel.apps.articles.views.article import (
    PostListView,
    PostCreateView,
    PostDeleteView,
    PostUpdateView,
    post_share,
    reply_page,
    post_detail,
    contact_form,
)


app_name = "blog"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>", post_detail, name="post-detail"),
    path("post/update/<int:pk>/", PostUpdateView.as_view(), name="post-update"),
    path("post/delete/<int:pk>/", PostDeleteView.as_view(), name="post-delete"),
    path("comment/reply/", reply_page, name="reply"),
    path("contact/", contact_form, name="contact"),
    path("<int:post_id>/share/", post_share, name="post_share"),
]
