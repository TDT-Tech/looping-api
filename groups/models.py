from django.db import models

from users.models import User


class Group(models.Model):
    class Schedule(models.TextChoices):
        BIWEEKLY = "BIWEEKLY"
        QUARTERLY = "QUARTERLY"
        MONTHLY = "MONTHLY"

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False)
    active = models.BooleanField(default=True)
    schedule = models.CharField(choices=Schedule.choices, default=Schedule.BIWEEKLY)
    logo_url = models.TextField(blank=True, null=True)
    last_issue_date = models.DateField(blank=True, null=True)
    users = models.ManyToManyField(User, through="Member")

    def __str__(self):
        return self.name


class Member(models.Model):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN"
        MEMBER = "MEMBER"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(choices=Roles.choices, blank=False)
