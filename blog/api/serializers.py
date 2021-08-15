from blog.models import Blog, Comment

from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = ['id',
                  'title',
                  'short_description',
                  'image',
                  'user',
                  'full_description',
                  'rating',
                  'posted',
                  'publish',
                  'comments']

    def get_comments(self, obj):
        qs = Comment.objects.filter(post=obj).count()
        return qs


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
