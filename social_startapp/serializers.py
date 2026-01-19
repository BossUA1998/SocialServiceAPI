from django.db import transaction
from rest_framework import serializers

from social_startapp.models import Subscriber, Post, Comment, HashTag
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


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ("id", "name")


class MyPostsSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source="who_liked.count", read_only=True)
    hashtags = HashTagSerializer(many=True)

    class Meta:
        model = Post
        fields = ["id", "created_at", "text", "likes", "hashtags"]

    @staticmethod
    def _raw_tags_to_iter_obj(raw_tags: str) -> map:
        return map(
            lambda x: (
                x["name"].strip().lower()
                if x["name"].startswith("#")
                else "#" + x["name"].strip().lower()
            ),
            raw_tags,
        )

    def create(self, validated_data):
        with transaction.atomic():
            hashtags = validated_data.pop("hashtags", None)
            post = Post.objects.create(**validated_data)

            if hashtags:
                for hashtag in self._raw_tags_to_iter_obj(hashtags):
                    _ht, _ = HashTag.objects.get_or_create(name=hashtag)
                    post.hashtags.add(_ht)
            return post

    def update(self, instance, validated_data):
        raw_tags = validated_data.pop("hashtags", None)

        post = super().update(instance, validated_data)
        post.hashtags.set(
            HashTag.objects.get_or_create(name=tag)[0]
            for tag in self._raw_tags_to_iter_obj(raw_tags)
        )

        return post


class PostsSerializer(MyPostsSerializer):
    author = AnyUserSerializer(read_only=True)
    hashtags = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=True
    )

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
