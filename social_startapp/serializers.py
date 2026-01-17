from rest_framework import serializers

from social_startapp.models import Subscriber, Post, Comment
from user.serializers import AnyUserSerializer


class SubscriptionsSerializer(serializers.ModelSerializer):
    author = AnyUserSerializer(read_only=True)

    class Meta:
        model = Subscriber
        fields = ("id", "author")


class FollowersSerializer(serializers.ModelSerializer):
    subscriber = AnyUserSerializer(read_only=True)

    class Meta:
        model = Subscriber
        fields = ("id", "subscriber")


class CommentSerializer(serializers.ModelSerializer):
    author = AnyUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "text", "created_at")


class PostsSerializer(serializers.ModelSerializer):
    author = AnyUserSerializer(read_only=True)
    likes = serializers.IntegerField(source="who_liked.count", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "created_at",
            "text",
            "author",
            "likes",
            "comments",
        )
