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


class MyPostsSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source="who_liked.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "created_at",
            "text",
            "likes",
            # "hashtags"
        ]


class PostsSerializer(MyPostsSerializer):
    author = AnyUserSerializer(read_only=True)

    class Meta(MyPostsSerializer.Meta):
        fields = MyPostsSerializer.Meta.fields + [
            "author",
        ]


class PostsDetailSerializer(PostsSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PostsSerializer.Meta):
        fields = PostsSerializer.Meta.fields + [
            "comments",
        ]
