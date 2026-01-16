from rest_framework import mixins, viewsets

from social_startapp.models import Subscriber
from social_startapp.serializers import SubscriptionsSerializer, FollowersSerializer


class MySubscribeView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        return self.request.user.subscriptions.all()


class SubscribersView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FollowersSerializer

    def get_queryset(self):
        return self.request.user.followers.all()
