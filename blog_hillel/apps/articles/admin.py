from django.contrib import admin

from .models import Blog, Comment


def make_moderated(queryset):
    queryset.update(moderated=True)


make_moderated.short_description = "Mark selected comments as moderated"  # noqa:E305


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ["post", "name", "email", "text", "active"]
    list_display = ("name", "text", "active")
    list_filter = ("active", "name")
    actions = [make_moderated]


class CommentInlineModelAdmin(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""

    model = Comment


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "publish", "posted")
    fields = [
        "title",
        "short_description",
        "image",
        "user",
        "full_description",
        "posted",
        "publish",
    ]
    inlines = [CommentInlineModelAdmin]
    list_filter = ("posted", "publish", "user")
    search_fields = ("title", "full_description")
    prepopulated_fields = {"short_description": ("title",)}
    raw_id_fields = ("user",)
    date_hierarchy = "publish"
    ordering = ("publish",)
