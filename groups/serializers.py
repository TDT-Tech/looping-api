from rest_framework import serializers

from groups.models import Group, Member
from newsletters.models import Newsletter
from utils.utils import calculate_next_issue_date


class MemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name")

    class Meta:
        model = Member
        fields = ("name", "role")


class GroupSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "active",
            "schedule",
            "logo_url",
            "last_issue_date",
            "members",
        )

    def create(self, validated_data):
        user = validated_data.pop("user")
        group = Group.objects.create(**validated_data)
        Member.objects.create(user_id=user.id, group=group, role=Member.Roles.ADMIN)

        return group

    def update(self, instance, validated_data):
        current_schedule = instance.schedule
        new_schedule = validated_data.get("schedule", instance.schedule)
        updated_instance = super().update(instance, validated_data)

        # If we change the schedule of a group, need to update
        # the schedule of any upcoming newsletters
        if current_schedule != new_schedule:
            newsletters_to_update = Newsletter.objects.filter(
                group_id=instance.id, status=Newsletter.Status.UPCOMING
            ).order_by("issue_date")
            prev_issue_date = newsletters_to_update.first().issue_date
            for newsletter in newsletters_to_update:
                new_issue_date = calculate_next_issue_date(
                    new_schedule, prev_issue_date
                )
                newsletter.issue_date = new_issue_date
                prev_issue_date = new_issue_date
            Newsletter.objects.bulk_update(newsletters_to_update, ["issue_date"])

        return updated_instance

    def get_members(self, obj):
        members = Member.objects.filter(group_id=obj.id)
        return MemberSerializer(members, many=True).data
