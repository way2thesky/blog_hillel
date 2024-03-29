from django import template
from django.utils.safestring import mark_safe

import markdown
from blog_hillel.apps.articles.models import Blog


register = template.Library()


@register.simple_tag
def total_posts():
    return Blog.published.count()


@register.inclusion_tag("articles/post_latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Blog.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
