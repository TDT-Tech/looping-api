from django.contrib.auth.backends import ModelBackend
from django.core import signing
from rest_framework import exceptions

from groups.models import Group, Member
from users.models import User


class MagicLinkBackend(ModelBackend):
    def authenticate(self, request):
        """
        Authenticates the given `email` provided in the token. If `email` does not
        exist, creates a new `user` instead and adds them to a group if `group_id`
        is provided.
        """
        try:
            token = request.GET.get("token", None)
            # Verify if token is valid
            data = signing.loads(token, max_age=900)

            email = data["email"]
            user = User.objects.filter(email=email).first()
            # If user with email doesn't exist, create one
            if not user:
                name = data["name"]
                user = User.objects.create_user(email=email, name=name)
                group_id = data.get("group_id", None)
                if group_id and Group.objects.get(id=group_id):
                    Member.objects.create(
                        user=user, group_id=group_id, role=Member.Roles.MEMBER
                    )

            return user
        except Exception:
            raise exceptions.AuthenticationFailed(detail="Invalid or expired token")

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
