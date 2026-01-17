from django.urls import path, include
from rest_framework.routers import DefaultRouter

from social_startapp.views import (
    MySubscribeView,
    SubscribersView,
    PostsViewSet,
    MyPostsViewSet,
)

router = DefaultRouter()
router.register("subscriptions", MySubscribeView, basename="subscriptions")
router.register("followers", SubscribersView, basename="followers")
router.register("my_posts", MyPostsViewSet, basename="my_posts")

post_list = PostsViewSet.as_view({"get": "list", "post": "create"})
post_detail = PostsViewSet.as_view(
    {"get": "retrieve", "post": "like", "put": "update", "patch": "partial_update"}
)
comment = PostsViewSet.as_view(
    {
        "post": "comment",
    }
)

urlpatterns = [
    path("", include(router.urls)),
    path("posts/", post_list, name="post-list"),
    path("posts/<int:pk>/", post_detail, name="post-detail"),
    path("posts/<int:pk>/comment/", comment, name="comment"),
]

app_name = "social_startapp"
