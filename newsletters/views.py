from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from groups.models import Group
from newsletters.models import Answer, Newsletter, Question
from newsletters.permissions import IsGroupMember, NewsletterAdminAllMemberReadOnly
from newsletters.serializers import (
    AnswerCreateSerializer,
    AnswerSerializer,
    NewsletterSerializer,
    QuestionCreateSerializer,
    QuestionSerializer,
)
from utils.utils import get_membership


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [NewsletterAdminAllMemberReadOnly]

    def get_queryset(self):
        user_groups = Group.objects.filter(users=self.request.user).values_list(
            "id", flat=True
        )
        return self.queryset.filter(group_id__in=user_groups)

    @action(detail=True, methods=["GET"])
    def questions(self, request, pk=None):
        newsletter = self.get_object()
        questions = newsletter.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    @action(
        detail=True, methods=["DELETE"], url_path="questions/(?P<question_pk>[^/.]+)"
    )
    def remove_question(self, request, question_pk, pk=None):
        newsletter = self.get_object()
        if newsletter.status in (
            Newsletter.Status.UPCOMING,
            Newsletter.Status.INPROGRESS,
        ):
            question = get_object_or_404(newsletter.questions, pk=question_pk)
            newsletter.questions.remove(question)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                "message": "Unable to remove questions for Inactive or Delivered \
                Newsletter"
            },
        )

    @action(detail=True, methods=["POST"], url_path="questions/batch")
    def batch_questions(self, request, pk=None):
        newsletter = self.get_object()
        if newsletter.status in (
            Newsletter.Status.UPCOMING,
            Newsletter.Status.INPROGRESS,
        ):
            serializer = QuestionCreateSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)

            author = request.user.name
            new_questions = []
            for question in serializer.data:
                new_question = Question(
                    question=question["question"], author=author, group=newsletter.group
                )
                new_questions.append(new_question)

            created_questions = Question.objects.bulk_create(new_questions)
            newsletter.questions.add(*created_questions)
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                "message": "Can't add questions for Inactive or Delivered newsletter"
            },
        )


class AnswerViewSet(viewsets.ViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsGroupMember]

    def dispatch(self, request, *args, **kwargs):
        req = self.initialize_request(request, *args, **kwargs)
        newsletter_id = self.kwargs["newsletter_id"]
        self.newsletter = (
            Newsletter.objects.prefetch_related("group")
            .filter(id=newsletter_id)
            .first()
        )
        if not self.newsletter:
            return HttpResponseNotFound(f"Newsletter with id {newsletter_id} not found")
        # object permissions aren't ran for list methods, need to manually check here
        # for list endpoint
        membership = get_membership(self.newsletter.group, req.user)
        if not membership:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(
            newsletter_id=self.kwargs["newsletter_id"], submitter=user
        )

    def list(self, request, **kwargs):
        answers = self.get_queryset()
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST", "PUT"])
    def batch(self, request, **kwargs):
        serializer = (
            AnswerCreateSerializer(data=request.data, many=True)
            if request.method == "POST"
            else AnswerSerializer(data=request.data, many=True)
        )
        serializer.is_valid(raise_exception=True)

        # Check if newsletter is valid to add answers to.
        if self.newsletter.status != Newsletter.Status.INPROGRESS:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "Newsletter is not in progress"},
            )

        # We want to bulk create new answers with POST
        if request.method == "POST":
            answers = []
            submitter = request.user
            # Check if answers to be added are for questions in the newsletter
            question_ids = set(answer["question_id"] for answer in serializer.data)
            questions_in_newsletters = set(
                self.newsletter.questions.all().values_list("id", flat=True)
            )
            if not question_ids.issubset(questions_in_newsletters):
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": "Questions not found in newsletter"},
                )
            for answer in serializer.data:
                new_answer = Answer(
                    question_id=answer["question_id"],
                    answer=answer["answer"],
                    submitter=submitter,
                    newsletter_id=self.newsletter.id,
                )
                answers.append(new_answer)
            Answer.objects.bulk_create(answers)
            return Response(status=status.HTTP_201_CREATED)
        # Otherwise bulk update existing answers with PUT
        else:
            answer_data = {a["id"]: a["answer"] for a in serializer.data}
            answers = {
                a.id: a
                for a in self.get_queryset().filter(
                    id__in=answer_data.keys(), submitter=request.user
                )
            }
            updated_answers = []
            for answer_id, updated_answer in answer_data.items():
                answer = answers.get(answer_id, None)
                if answer:
                    answer.answer = updated_answer
                    updated_answers.append(answer)
            Answer.objects.bulk_update(updated_answers, fields=["answer"])
            return Response(status=status.HTTP_200_OK)
