import datetime

from rest_framework import serializers

from newsletters.models import Answer, Newsletter, Question
from users.models import User
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


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("question",)


class NewsletterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ("status", "group", "questions")

    def create(self, validated_data):
        questions = validated_data.pop("questions")
        group = validated_data["group"]

        last_newsletter = (
            Newsletter.objects.filter(group_id=group.id).order_by("-issue_date").first()
        )
        last_issue_date = (
            datetime.date.today() if not last_newsletter else last_newsletter.issue_date
        )
        validated_data["issue_date"] = calculate_next_issue_date(
            group.schedule, last_issue_date
        )

        inprogress_newsletter = Newsletter.objects.filter(
            group_id=group.id, status=Newsletter.Status.INPROGRESS
        ).first()
        if not inprogress_newsletter:
            validated_data["status"] = Newsletter.Status.INPROGRESS

        newsletter = Newsletter.objects.create(**validated_data)
        newsletter.questions.set(questions)
        return newsletter


class NewsletterSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Newsletter
        fields = ("id", "status", "issue_date", "group", "questions")

    def update(self, instance, validated_data):
        previous_status = instance.status
        instance.status = validated_data.get("status", instance.status)
        instance.issue_date = validated_data.get("issue_date", instance.issue_date)
        # Only update questions for Upcoming or In-Progress newsletters
        if instance.status in (
            Newsletter.Status.UPCOMING,
            Newsletter.Status.INPROGRESS,
        ):
            questions_to_add = validated_data.pop("questions", [])
            # Check if any questions removed from newsletter and delete existing answers
            questions_in_newsletter = set(
                instance.questions.all().values_list("id", flat=True)
            )
            question_ids = set(q["id"] for q in questions_to_add)
            removed_questions_ids = questions_in_newsletter - question_ids
            for question_id in removed_questions_ids:
                Answer.objects.filter(
                    question_id=question_id, newsletter_id=instance.id
                ).delete()

            questions = []
            for question in questions_to_add:
                q = Question.objects.filter(pk=question["id"]).first()
                if q:
                    questions.append(q)
            instance.questions.set(questions)
        instance.save()
        # If we make an inprogress newsletter inactive, need to
        # mark another newsletter as inprogress
        if (
            previous_status == Newsletter.Status.INPROGRESS
            and instance.status == Newsletter.Status.INACTIVE
        ):
            next_newsletter = (
                Newsletter.objects.filter(
                    group_id=instance.group.id, status=Newsletter.Status.UPCOMING
                )
                .order_by("issue_date")
                .first()
            )
            if next_newsletter:
                next_newsletter.status = Newsletter.Status.INPROGRESS
                next_newsletter.save()

        return instance


class AnswerCreateSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

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

    def validate_submitter(self, submitter_id):
        try:
            data = User.objects.get(email=submitter_id)
        except Exception as e:
            raise serializers.ValidationError(
                f"{e}: User with {submitter_id} doesn't exist"
            )
        return data
