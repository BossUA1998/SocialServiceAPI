from django.urls import path, include
from rest_framework.routers import DefaultRouter

from social_startapp.views import MySubscribeView, SubscribersView

router = DefaultRouter()
router.register("subscriptions", MySubscribeView, basename="subscriptions")
router.register("followers", SubscribersView, basename="followers")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "social_startapp"
