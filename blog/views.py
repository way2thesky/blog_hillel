from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView

from blog.forms import RegisterForm, CommentForm
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, get_user_model

from blog.models import Post, Comment

User = get_user_model()


def index(request):
    """View function for home page of site."""

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


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'short_description', 'full_description', 'posted']
    template_name = 'post_create.html'
    success_url = reverse_lazy('blog:post-list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        self.object = post
        return HttpResponseRedirect(self.get_success_url())


class PostList(ListView):
    model = Post
    paginate_by = 10
    template_name = 'post_list.html'


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, posted=True)
    comments = Comment.objects.all().filter(post=post).filter(moderated=True)
    paginator = Paginator(comments, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():
            comm = Comment()
            comm.username = form.cleaned_data['username']
            comm.text = form.cleaned_data['text']
            comm.post = post
            comm.save()
            return HttpResponseRedirect(reverse('post-detail', args=(post.id,)))

    else:
        initial = {'username': request.user.username}
        form = CommentForm(initial=initial)

    context = {
        'form': form,
        'post': post,
        'page_obj': page_obj,
    }

    return render(request, 'post_detail.html', context)
