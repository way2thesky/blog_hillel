from blog.api import views

from django.urls import path

app_name = "blog_api"


urlpatterns = [
    path('', views.PostAPIView.as_view()),
    path('register/', views.RegisterUser.as_view()),
]
