import os
import uuid

from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager as AbstractUserManager,
)
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def _uuid_photo_save(instance: "User", filename: str) -> str:
    _, ext = os.path.splitext(filename)

    return os.path.join(
        "user_images/",
        f"{instance.pk}-{uuid.uuid4()}{ext}",
    )


def _get_default_username():
    return f"no_search-{uuid.uuid4()}"


class UserManager(AbstractUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is False:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is False:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=52, default=_get_default_username())
    email = models.EmailField(_("email address"), unique=True)
    image = models.ImageField(blank=True, upload_to=_uuid_photo_save)
    biography = models.TextField(blank=True, max_length=512)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
