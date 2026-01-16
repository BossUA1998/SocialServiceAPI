from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscriber(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )

    class Meta:
        unique_together = ("subscriber", "author")
