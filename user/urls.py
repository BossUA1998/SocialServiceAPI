from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import CreateUserView, LogoutView, ManageUserView, AnyUserView

router = DefaultRouter()
router.register("", AnyUserView, basename="user")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create_user"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="account_user"),
    path("logout/", LogoutView.as_view(), name="logout_user"),
    path("", include(router.urls)),
]

app_name = "user"
