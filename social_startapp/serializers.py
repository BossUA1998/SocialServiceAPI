from rest_framework import serializers

from social_startapp.models import Subscriber
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
