from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    User model manager where email is the unique id for auth
    instead of usernames.
    """

    def create_user(self, email, name, password, **extra_fields):
        """
        Create and save a user with the given email and password
        """
        if not email or not name:
            raise ValueError("Email and name is required")
        email = self.normalize_email(email)

        if password is not None:
            user = self.model(email=email, name=name, password=password, **extra_fields)
            user.save()
        else:
            user = self.model(email=email, name=name, **extra_fields)
            user.set_unusable_password()
            user.save()
        return user

    def create_superuser(self, email, name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        user = self.create_user(email, name, password, **extra_fields)
        user.set_password(password)
        user.save()

        return user
