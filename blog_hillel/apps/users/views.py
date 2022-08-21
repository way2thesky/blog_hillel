from typing import List

from django.contrib.auth import get_user_model
from django.views import generic
from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from blog_hillel.apps.articles.models import Blog

__all__: List[str] = ["UserListView", "UserDetailView"]

User = get_user_model()


class UserListView(ListView):
    model = User

    template_name = "users/user_list.html"
    paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class UserDetailView(generic.ListView):
    model = Blog
    paginate_by = 5
    template_name = "users/user_detail.html"
    success_message = "Profile Updated"

    def get_queryset(self):
        id = self.kwargs["pk"]  # noqa A001
        target_user = get_object_or_404(User, pk=id)
        return Blog.objects.filter(user=target_user)

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context["users"] = get_object_or_404(User, pk=self.kwargs["pk"])
        return context
