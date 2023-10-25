from rest_framework import serializers

from groups.models import Group
from groups.serializers import GroupSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "groups", "email"]

    def get_groups(self, obj):
        groups = Group.objects.filter(member__user_id=obj.id)
        return GroupSerializer(groups, many=True).data
