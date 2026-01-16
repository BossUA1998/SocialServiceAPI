from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer, LogoutSerializer


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh_token"]

        try:
            token = RefreshToken(refresh_token)
            if int(token["user_id"]) == request.user.id:
                token.blacklist()
            else:
                return Response(
                    {"error": "Not your token"}, status=status.HTTP_403_FORBIDDEN
                )
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)


class CreateUserView(generics.GenericAPIView):
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class ManageUserView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class AnyUserView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs["pk"]:
            return redirect("user:account_user")
        return super().get(request, *args, **kwargs)

    def get_object(self):
        user = get_object_or_404(get_user_model(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, user)

        return user
