from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from utils.tests.factory import UserFactory


# Create your tests here.
class UsersManagersTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="normal@user.com", name="Tommy Nguyen")
        self.assertEqual(user.email, "normal@user.com")
        self.assertEqual(user.name, "Tommy Nguyen")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", name="Tommy Nguyen")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="normal@user.com", name="")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo", name="Tommy Nguyen"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertEqual(admin_user.name, "Tommy Nguyen")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com",
                password="foo",
                name="Tommy Nguyen",
                is_superuser=False,
            )


class IsOwnerPermissionTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.second_user = UserFactory(email="test@test.com")
        self.url = "/users/{}/"
        self.client.force_authenticate(user=self.user)

    def test_user_can_access_self(self):
        response = self.client.get(self.url.format(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_access_other_user(self):
        response = self.client.get(self.url.format(self.second_user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_update_self(self):
        update_data = {"name": "Updated", "email": self.user.email}
        response = self.client.put(
            self.url.format(self.user.id),
            data=update_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["name"], update_data["name"])

    def test_user_cant_update_other_user(self):
        response = self.client.put(
            self.url.format(self.second_user.id),
            data={"name": "updated", "email": self.second_user.email},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_self(self):
        response = self.client.delete(self.url.format(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_other_user(self):
        response = self.client.delete(self.url.format(self.second_user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
