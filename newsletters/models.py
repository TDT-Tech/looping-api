from django.db import models

from groups.models import Group
from users.models import User


class Question(models.Model):
    question = models.TextField()
    author = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)


class Newsletter(models.Model):
    class Status(models.TextChoices):
        UPCOMING = "UPCOMING"
        INPROGRESS = "INPROGRESS"
        DELIVERED = "DELIVERED"
        INACTIVE = "INACTIVE"

    status = models.CharField(choices=Status.choices, default=Status.UPCOMING)
    issue_date = models.DateField(blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)


class Answer(models.Model):
    answer = models.TextField()
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
