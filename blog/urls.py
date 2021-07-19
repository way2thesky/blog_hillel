from django.urls import path

from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/create/', views.PostCreate.as_view(), name='post-create'),
    path('posts/', views.PostList.as_view(), name='post-list'),
path('posts/<int:pk>/', views.post_detail, name='post-detail'),
]