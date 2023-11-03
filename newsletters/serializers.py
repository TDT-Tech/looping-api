import datetime

from rest_framework import serializers

from groups.models import Group
from newsletters.models import Answer, Newsletter, Question
from utils.utils import calculate_next_issue_date


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "id",
            "question",
            "author",
        )


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(slug_field="question", read_only=True)
    newsletter = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ("id", "answer", "submitter", "question", "newsletter")


class NewsletterSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    group = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Newsletter
        fields = ("id", "status", "issue_date", "group", "questions")

    def create(self, validated_data):
        group_id = validated_data["group"]
        group = Group.objects.get(group_id=group_id)
        last_issue_date = (
            group.last_issue_date.date() if group.last_issue_date else datetime.date()
        )

        validated_data["issue_date"] = calculate_next_issue_date(
            group.schedule, last_issue_date
        )
        newsletter = Newsletter.objects.create(**validated_data)

        return newsletter
