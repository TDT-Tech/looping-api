from rest_framework import serializers

from groups.models import Group, Member


class MemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name")

    class Meta:
        model = Member
        fields = ("name", "role")


class GroupSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "active",
            "schedule",
            "logo_url",
            "last_issue_date",
            "members",
        ]

    def create(self, validated_data):
        user = validated_data.pop("user")
        group = Group.objects.create(**validated_data)
        Member.objects.create(user_id=user.id, group=group, role=Member.Roles.ADMIN)

        return group

    def get_members(self, obj):
        members = Member.objects.filter(group_id=obj.id)
        return MemberSerializer(members, many=True).data
