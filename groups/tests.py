from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from groups.models import Member
from utils.tests.factory import UserFactory


class GroupViewSetTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_user_creating_group_creates_membership(self):
        url = reverse("group-list")
        data = {"name": "test group"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "test group")
        members = self.user.member_set.filter(group_id=response.data["id"])
        self.assertIsNotNone(members)
        for member in members:
            self.assertEqual(member.user_id, self.user.id)
            self.assertEqual(member.role, Member.Roles.ADMIN)
