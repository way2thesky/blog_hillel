from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),

    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('post/create/', views.PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>', views.PostDetail.as_view(), name='post-detail'),

    # path('blogs/update/<int:pk>/', views.PostUpdate.as_view(), name='post-update'),
    # path('blogs/delete/<int:pk>/', views.PostDelete.as_view(), name='post-delete'),

    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('author/<int:pk>', views.BlogListbyAuthorView.as_view(), name='author-detail'),

    # path('my-blogs/', views.blogger_posts, name='author-posts'),
    # path('blog/<int:pk>/comment/', views.BlogCommentCreate.as_view(), name='blog-comment'),
    #
    # path('feedback', views.feedback_form, name="feedback"),
]
