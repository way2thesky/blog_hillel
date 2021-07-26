from blog.forms import CommentForm, ContactForm, RegisterForm
from blog.models import Blog, BlogComment

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView


User = get_user_model()


def index(request):
    return render(request, 'index.html')


class RegisterFormView(SuccessMessageMixin, FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('blog:index')
    success_message = 'Profile created'

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
    success_message = 'Profile updated'

    def get_success_url(self):
        return reverse('blog:user-detail', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class PostCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'short_description', 'image', 'full_description', 'posted']
    template_name = 'post_create.html'
    success_url = reverse_lazy('blog:post-list')
    success_message = 'Post created'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        self.object = post
        return HttpResponseRedirect(self.get_success_url())


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'short_description', 'image', 'full_description', 'posted']
    success_url = reverse_lazy('blog:post-list')
    template_name = 'post_update_page.html'
    login_url = reverse_lazy('login')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('blog:index')
    model = Blog
    success_url = reverse_lazy('blog:post-list')


@method_decorator(cache_page(20), name='dispatch')
class PostListView(generic.ListView):
    model = Blog
    paginate_by = 5
    template_name = 'post_list.html'

    def get_queryset(self):
        return Blog.objects.all().filter(posted=True)


class PostDetail(DetailView):
    model = Blog
    context_object_name = "post"
    template_name = "post_detail.html"


def post_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk, posted=True)

    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Comment sent')
            return HttpResponseRedirect(reverse('blog:post-detail', args=(post.id,)))
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Blog.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:6]

    return render(request, 'post_detail.html',
                  {'post': post, 'comments': comments, 'comment_form': comment_form, 'similar_posts': similar_posts})


class UserListView(ListView):
    model = User

    template_name = 'user_list.html'
    paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class UserDetailView(generic.ListView):
    model = Blog
    paginate_by = 5
    template_name = 'user_detail.html'
    success_message = 'Profile Updated'

    def get_queryset(self):
        id = self.kwargs['pk']  # noqa A001
        target_user = get_object_or_404(User, pk=id)
        return Blog.objects.filter(user=target_user)

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['users'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context


def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)

        # print(form)

        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input

            print(post_id)  # noqa T001
            print(parent_id)  # noqa T001
            print(post_url)  # noqa T001

            reply = form.save(commit=False)

            reply.post = Blog(id=post_id)
            reply.parent = BlogComment(id=parent_id)
            reply.save()

            return HttpResponseRedirect(reverse('blog:post-detail', args=(post_id,)))

    return redirect("/")


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'yii2_loc@ukr.net',
                             ['matroskin978@gmail.com'], fail_silently=True)
            if mail:
                messages.success(request, 'Successful! Sent')
                return redirect('blog:index')
            else:
                messages.error(request, 'Some Errors')
        else:
            messages.error(request, 'Some Error with validation')
    else:
        form = ContactForm()
    return render(request, 'contact_form.html', {"form": form})
