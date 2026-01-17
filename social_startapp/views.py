from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from social_startapp.models import Subscriber, Post, Comment
from social_startapp.permissions import IsAuthorOrReadOnly
from social_startapp.serializers import (
    SubscriptionsSerializer,
    FollowersSerializer,
    PostsSerializer,
    CommentSerializer,
)
from user.serializers import EmptySerializer


class MySubscribeView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        return self.request.user.subscriptions.all()


class SubscribersView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FollowersSerializer

    def get_queryset(self):
        return self.request.user.followers.all()


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        return self.queryset.filter(
            author__in=self.request.user.subscriptions.values_list("author")
        )

    def get_serializer_class(self):
        if self.action == "like":
            return EmptySerializer
        return PostsSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def like(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user in obj.who_liked.all():
            obj.who_liked.remove(request.user)
        else:
            obj.who_liked.add(self.request.user)
        return Response(status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="comment",
    )
    def comment(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=self.get_object())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # if self.request.method == "DELETE":
        #     self.get_object().delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        # if self.request.method == "POST":
        #     print(kwargs)
        #     serializer = CommentSerializer(data=request.data)
        # else:
        #     serializer = CommentSerializer(
        #         data=request.data, instance=self.get_object()
        #     )
        # if serializer.is_valid():
        #     serializer.save(author=self.request.user, post=self.get_object())
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyPostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostsSerializer

    def get_queryset(self):
        return self.request.user.posts.all()
