from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import BlogComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['username', 'description']


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
