from django.urls import path
from blog.api import views
app_name = "blog_api"


urlpatterns = [
    path('', views.PostAPIView.as_view()),
    path('register/', views.RegisterUser.as_view()),
]
