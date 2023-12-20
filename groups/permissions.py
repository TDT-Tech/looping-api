from rest_framework import permissions

from groups.models import Member


class AdminAllButMemberReadOnly(permissions.BasePermission):
    restricted_methods = ("PUT", "PATCH", "DELETE")

    def get_membership(self, obj, user):
        return obj.member_set.filter(user=user).first()

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        membership = self.get_membership(obj, request.user)

        if membership:
            if request.method in permissions.SAFE_METHODS:
                return True

            if (
                membership.role is Member.Roles.ADMIN
                and request.method in self.restricted_methods
            ):
                return True

        return False
