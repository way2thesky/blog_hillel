from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),

    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blogs/create/', views.PostCreate.as_view(), name='blog-create'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),

    # path('blogs/update/<int:pk>/', views.PostUpdate.as_view(), name='blog-update'),
    # path('blogs/delete/<int:pk>/', views.PostDelete.as_view(), name='blog-delete'),

    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    # path('blogger/<int:pk>', views.BlogListbyAuthorView.as_view(), name='blogger-detail'),

    # path('my-blogs/', views.blogger_posts, name='blogger-posts'),
    # path('blog/<int:pk>/comment/', views.BlogCommentCreate.as_view(), name='blog-comment'),
    #
    # path('feedback', views.feedback_form, name="feedback"),
]
