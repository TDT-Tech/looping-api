import datetime

from rest_framework import serializers

from newsletters.models import Answer, Newsletter, Question
from utils.utils import calculate_next_issue_date


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Question
        fields = (
            "id",
            "question",
            "author",
        )
        extra_kwargs = {"id": {"required": False}}


class NewsletterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ("status", "group", "questions")

    def create(self, validated_data):
        questions = validated_data.pop("questions")
        group = validated_data["group"]
        last_issue_date = (
            group.last_issue_date.date()
            if group.last_issue_date
            else datetime.date.today()
        )

        validated_data["issue_date"] = calculate_next_issue_date(
            group.schedule, last_issue_date
        )
        newsletter = Newsletter.objects.create(**validated_data)
        newsletter.questions.set(questions)
        return newsletter


class NewsletterSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Newsletter
        fields = ("id", "status", "issue_date", "group", "questions")

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.issue_date = validated_data.get("issue_date", instance.issue_date)
        questions_to_add = validated_data.pop("questions")
        questions = []
        for question in questions_to_add:
            q = Question.objects.get(pk=question["id"])
            questions.append(q)
        instance.questions.set(questions)
        instance.save()
        return instance


class AnswerCreateSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()

    class Meta:
        model = Answer
        fields = (
            "answer",
            "question_id",
        )


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    id = serializers.IntegerField()

    class Meta:
        model = Answer
        fields = ("id", "answer", "submitter", "question")
