from django.urls import path

from . import views
from .views import contact

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),

    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('post/create/', views.PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>', views.post_detail, name='post-detail'),

    # path('blogs/update/<int:pk>/', views.PostUpdate.as_view(), name='post-update'),
    # path('blogs/delete/<int:pk>/', views.PostDelete.as_view(), name='post-delete'),

    path('users/', views.UserListView.as_view(), name='user-list'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    # path('my-blogs/', views.blogger_posts, name='author-posts'),
    # path('blog/<int:pk>/comment/', views.BlogCommentCreate.as_view(), name='blog-comment'),
    #
    # path('feedback', views.feedback_form, name="feedback"),
    path('comment/reply/', views.reply_page, name="reply"),
    path('contact/', contact, name='contact'),
]
