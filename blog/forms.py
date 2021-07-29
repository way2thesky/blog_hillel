from captcha.fields import CaptchaField

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'text')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name', 'class': 'form-control'}
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class': 'form-control'}
        self.fields['text'].widget.attrs = {'placeholder': 'Comment here...', 'class': 'form-control', 'rows': '5'}


class ContactForm(forms.Form):
    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))
    email = forms.EmailField(required=True)
    captcha = CaptchaField()
