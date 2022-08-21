from django.conf import settings
from django.views import generic
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.views.generic import FormView, CreateView, DeleteView, UpdateView

from blog_hillel.apps.articles.models import Blog, Comment
from blog_hillel.apps.articles.forms import (
    CommentForm,
    ContactForm,
    RegisterForm,
    EmailBlogForm,
)


User = get_user_model()


def index(request):
    return render(request, "articles/index.html")


class RegisterFormView(SuccessMessageMixin, FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("index")
    success_message = "Profile created"

    def form_valid(self, form):
        form.save()

        username = self.request.POST["username"]
        password = self.request.POST["password1"]
        user = authenticate(username=username, password=password)
        login(self.request, user)
        send_mail(
            subject="Welcome to my BLOG",
            message=f"Hi {username}, thank you for registering in my Blog.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["random@example.com"],
            fail_silently=True,
        )

        return super(RegisterFormView, self).form_valid(form)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = "registration/update_profile.html"
    success_message = "Profile updated"

    def get_success_url(self):
        return reverse("users:user-detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ["title", "short_description", "image", "full_description", "posted"]
    template_name = "articles/post_create.html"
    success_url = reverse_lazy("blog:post-list")
    success_message = "Post created"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()

        send_mail(
            subject="New post",
            message=f"New {post} created! Check it on admin panel.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["admin@example.com"],
            fail_silently=True,
        )
        self.object = post
        return HttpResponseRedirect(self.get_success_url())


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ["title", "short_description", "image", "full_description", "posted"]
    success_url = reverse_lazy("blog:post-list")
    template_name = "articles/post_update_page.html"
    login_url = reverse_lazy("login")


class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy("index")
    model = Blog
    success_url = reverse_lazy("blog:post-list")
    template_name = "articles/post_delete_page.html"


@method_decorator(cache_page(20), name="dispatch")
class PostListView(generic.ListView):
    model = Blog
    paginate_by = 5
    template_name = "articles/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Blog.objects.all().filter(posted=True)


def post_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk, posted=True)
    comments = post.comments.filter(active=True)

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            messages.success(request, "Successful! Sent")
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(reverse("blog:post-detail", args=(post.id,)))
    else:
        comment_form = CommentForm()

    return render(
        request,
        "articles/post_detail.html",
        {"post": post, "comments": comments, "comment_form": comment_form},
    )


def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get("post_id")  # from hidden input
            parent_id = request.POST.get("parent")  # from hidden input
            post_url = request.POST.get("post_url")  # from hidden input
            messages.success(request, "Successful! Sent")
            print(post_id)  # noqa T001
            print(parent_id)  # noqa T001
            print(post_url)  # noqa T001

            reply = form.save(commit=False)

            reply.post = Blog(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return HttpResponseRedirect(reverse("blog:post-detail", args=(post_id,)))

    return redirect("/")


def contact_form(request):
    data = dict()
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["from_email"]
            message = form.cleaned_data["message"]
            data["form_is_valid"] = True
            contact_us.delay(subject, message, from_email)
            messages.add_message(request, messages.SUCCESS, "Message sent - SUCCESS")
        else:
            data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(
        template_name="blog_hillel/includes/contact.html",
        context=context,
        request=request,
    )
    return JsonResponse(data)


def post_share(request, post_id):
    post = get_object_or_404(Blog, id=post_id)
    sent = False

    if request.method == "POST":

        form = EmailBlogForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(subject, message, "admin@myblog.com", [cd["to"]])
            sent = True

    else:
        form = EmailBlogForm()
    return render(
        request, "articles/post_share.html", {"post": post, "form": form, "sent": sent}
    )
