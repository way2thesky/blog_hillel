from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView

from blog.forms import RegisterForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, get_user_model

from blog.models import Blog

User = get_user_model()


def index(request):
    return render(request, 'index.html')


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("blog:index")

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'registration/update_profile.html'
    success_url = reverse_lazy('blogs:index')
    success_message = 'Profile updated'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5
    template_name = 'blogs.html'


class BlogDetailView(generic.DetailView):
    model = Blog


class BloggerListView(ListView):
    model = User
    template_name = 'bloggers.html'
    paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class PostCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'short_description', 'full_description', 'posted']
    template_name = 'blog_create.html'
    success_url = reverse_lazy('blog:blogs')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        self.object = post
        return HttpResponseRedirect(self.get_success_url())
