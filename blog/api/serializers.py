from blog.models import Blog, Comment

from django.contrib.auth.models import User

from rest_framework import serializers

from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class BlogListSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "short_description",
            "image",
            "user",
            "full_description",
            "rating",
            "posted",
            "publish",
            "tags",
        ]

    def validate(self, data):
        if len(data['full_description']) < 5:
            raise serializers.ValidationError({"error": "body is too short"})
        return data
