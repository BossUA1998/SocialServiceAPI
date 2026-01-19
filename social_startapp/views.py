import re

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from social_startapp.models import Subscriber, Post, Comment
from social_startapp.permissions import IsAuthorOrReadOnly
from social_startapp.serializers import (
    SubscriptionsSerializer,
    FollowersSerializer,
    MyPostsSerializer,
    PostsSerializer,
    PostsDetailSerializer,
    CommentSerializer,
)
from django.db.models import Count
from user.serializers import EmptySerializer


class MySubscribeView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        return self.request.user.subscriptions.select_related("author")


class SubscribersView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FollowersSerializer

    def get_queryset(self):
        return self.request.user.followers.select_related("subscriber")


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated)

    @staticmethod
    def _hashtags_to_iter_obj(hashtags: str) -> map:
        return map(lambda x: "#" + x, hashtags.split(","))

    def get_queryset(self):
        if hashtags := self.request.query_params.get("hashtags"):
            print("ok")
            return self.queryset.filter(
                hashtags__name__in=self._hashtags_to_iter_obj(hashtags)
            ).exclude(author=self.request.user)

        self.queryset = (
            self.queryset.select_related("author")
            .prefetch_related("who_liked")
            .filter(author__followers__subscriber=self.request.user)
        )
        if self.action == "retrieve":
            return self.queryset.prefetch_related("comments__author")

        return self.queryset

    def get_serializer_class(self):
        if self.action == "like":
            return EmptySerializer
        if self.action == "retrieve":
            return PostsDetailSerializer
        return PostsSerializer

    def like(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user in obj.who_liked.all():
            obj.who_liked.remove(request.user)
        else:
            obj.who_liked.add(self.request.user)
        return Response(status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == "comment":
            return (IsAuthenticated(),)
        return super().get_permissions()

    @action(
        methods=["POST", "DELETE", "PUT"],
        detail=True,
        url_path="comment",
    )
    def comment(self, request, *args, **kwargs):
        post = self.get_object()
        comment_obj = post.comments.filter(author=request.user).first()

        if comment_obj:
            if request.method == "DELETE":
                comment_obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            elif request.method == "PUT":
                serializer = CommentSerializer(
                    comment_obj, data=request.data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "You have already commented on this post."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            if request.method == "POST":
                serializer = CommentSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
        )


class MyPostsViewSet(viewsets.ModelViewSet):
    serializer_class = MyPostsSerializer

    def get_queryset(self):
        return self.request.user.posts.prefetch_related("who_liked")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
