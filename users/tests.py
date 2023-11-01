from django.contrib.auth import get_user_model
from django.core import signing
from django.test import RequestFactory, TestCase
from rest_framework import exceptions

from groups.models import Group, Member
from users.authentication import MagicLinkBackend
from users.models import User


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


class MagicLinkBackendTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email="factory@email.com", name="factory")
        self.group = Group(name="Test Group")
        self.group.save()
        self.auth = MagicLinkBackend()

    def test_auth_user_who_doesnt_exist_creates_new_user(self):
        magic_link_data = {"email": "test@gmail.com", "name": "Test User"}
        token = signing.dumps(magic_link_data)
        request = self.factory.post(f"/login/?token={token}")

        self.auth.authenticate(request)

        created_user = User.objects.get(email=magic_link_data["email"])
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.name, magic_link_data["name"])

    def test_auth_user_who_doesnt_exist_with_group_id_creates_user_and_membership(
        self,
    ):
        magic_link_data = {
            "email": "test@gmail.com",
            "name": "Test User",
            "group_id": self.group.id,
        }
        token = signing.dumps(magic_link_data)
        request = self.factory.post(f"/login/?token={token}")

        self.auth.authenticate(request)

        user = User.objects.get(email=magic_link_data["email"])
        membership = Member.objects.get(user=user)

        self.assertIsNotNone(membership)
        self.assertEqual(membership.group.id, magic_link_data["group_id"])
        self.assertEqual(membership.role, Member.Roles.MEMBER)

    def test_auth_user_who_doesnt_exist_with_invalid_group_id_raises_exception(self):
        magic_link_data = {
            "email": "test@gmail.com",
            "name": "Test User",
            "group_id": 1000,
        }
        token = signing.dumps(magic_link_data)
        request = self.factory.post(f"/login/?token={token}")

        with self.assertRaises(exceptions.AuthenticationFailed):
            self.auth.authenticate(request)

    def test_auth_user_who_exists_returns_user(self):
        magic_link_data = {"email": self.user.email, "name": self.user.name}
        token = signing.dumps(magic_link_data)
        request = self.factory.post(f"/login/?token={token}")

        self.auth.authenticate(request)

        user = User.objects.get(email=magic_link_data["email"])

        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user.email)

    def test_auth_raises_exception_with_invalid_token(self):
        magic_link_data = {}
        token = signing.dumps(magic_link_data)
        request = self.factory.post(f"/login?token={token}")
        with self.assertRaises(exceptions.AuthenticationFailed):
            self.auth.authenticate(request)
