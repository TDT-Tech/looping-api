from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from groups.models import Member
from utils.tests.factory import GroupMemberFactory, UserFactory, UserWithGroupFactory


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


class AdminAllButMemberReadOnlyPermissionsTests(APITestCase):
    def setUp(self):
        self.user = UserWithGroupFactory()
        self.user_with_no_group = UserFactory(email="test@test.com")
        self.group_url = f"/groups/{self.user.group_set.first().id}/"
        self.update_payload = {"name": "Test Update Name"}

    def test_user_cannot_access_groups_without_membership(self):
        self.client.force_authenticate(user=self.user_with_no_group)
        response = self.client.get(self.group_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_access_group_with_membership(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.group_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_group_member_cannot_update_group(self):
        GroupMemberFactory(
            user=self.user_with_no_group, group=self.user.group_set.first()
        )
        self.client.force_authenticate(user=self.user_with_no_group)
        response = self.client.put(self.group_url, data=self.update_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_group_member_cannot_delete_group(self):
        GroupMemberFactory(
            user=self.user_with_no_group, group=self.user.group_set.first()
        )
        self.client.force_authenticate(user=self.user_with_no_group)
        response = self.client.delete(self.group_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_group_admin_can_update_group(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.group_url, data=self.update_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.group_set.first().name, self.update_payload["name"])

    def test_group_admin_can_delete_group(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.group_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(self.user.group_set.first())
