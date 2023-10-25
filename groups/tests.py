from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from groups.models import Member
from users.models import User


class GroupViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(name="test_user", email="test@test.com")
        self.client.force_authenticate(user=self.user)

    def test_user_creating_group_creates_membership(self):
        url = reverse("group-list")
        data = {"name": "test group"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "test group")
        members = Member.objects.filter(group_id=response.data["id"])
        self.assertIsNotNone(members)
        for member in members:
            self.assertEqual(member.user_id, self.user.id)
            self.assertEqual(member.role, Member.Roles.ADMIN)
