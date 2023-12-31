from django.contrib.auth import get_user_model
from django.test import TestCase

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
