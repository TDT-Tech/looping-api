from django.http import HttpResponseForbidden, HttpResponseNotFound
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from newsletters.models import Answer, Newsletter, Question
from newsletters.permissions import IsGroupMember, NewsletterAdminAllMemberReadOnly
from newsletters.serializers import (
    AnswerCreateSerializer,
    AnswerSerializer,
    NewsletterSerializer,
    QuestionSerializer,
)
from utils.utils import get_membership


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [NewsletterAdminAllMemberReadOnly]


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
        return self.queryset.filter(newsletter_id=self.kwargs["newsletter_id"])

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
            submitter = request.user.name
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
                a.id: a for a in self.get_queryset().filter(id__in=answer_data.keys())
            }
            updated_answers = []
            for answer_id, updated_answer in answer_data.items():
                answer = answers[answer_id]
                answer.answer = updated_answer
                updated_answers.append(answer)
            Answer.objects.bulk_update(updated_answers, fields=["answer"])
            return Response(status=status.HTTP_200_OK)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
