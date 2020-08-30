from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class MyUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Ticket(models.Model):
    title = models.CharField(max_length=300)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(default="")
    filed_by = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="filed_by"
    )
    assigned_to = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="assigned_to",
        blank=True,
        null=True,
        default=None,
    )
    completed_by = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="completed_by",
        blank=True,
        null=True,
        default=None,
    )
    NEW = "New"
    IN_PROGRESS = "In Progress"
    DONE = "Done"
    INVALID = "Invalid"
    STATUS_CHOICES = [
        (NEW, "New"),
        (IN_PROGRESS, "In Progress"),
        (DONE, "Done"),
        (INVALID, "Invalid"),
    ]
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default=NEW,
    )
