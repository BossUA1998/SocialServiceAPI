from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings


def _uuid_photo_save(instance: "User", filename: str) -> str:
    _, ext = os.path.splitext(filename)

    return os.path.join(
        "posts_images/",
        f"{instance.pk}-{uuid.uuid4()}{ext}",
    )


class Subscriber(models.Model):
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
    )

    class Meta:
        unique_together = ("subscriber", "author")


class HashTag(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip().lower()

            if not self.name.startswith("#"):
                self.name = "#" + self.name

        super().save(*args, **kwargs)


class Post(models.Model):
    text = models.TextField(max_length=1024)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, upload_to=_uuid_photo_save)
    who_liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_posts"
    )
    hashtags = models.ManyToManyField(HashTag, related_name="posts", blank=True)

    class Meta:
        ordering = ("created_at",)


class Comment(models.Model):
    text = models.TextField(max_length=512)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
