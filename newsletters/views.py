from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from newsletters.models import Answer, Newsletter, Question
from newsletters.serializers import (
    AnswerCreateSerializer,
    AnswerSerializer,
    NewsletterSerializer,
    QuestionSerializer,
)


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnswerViewSet(viewsets.ViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
        # We want to bulk create new answers with POST
        if request.method == "POST":
            answers = []
            submitter = request.user.name
            newsletter_id = self.kwargs["newsletter_id"]
            for answer in serializer.data:
                new_answer = Answer(
                    question_id=answer["question_id"],
                    answer=answer["answer"],
                    submitter=submitter,
                    newsletter_id=newsletter_id,
                )
                answers.append(new_answer)
            Answer.objects.bulk_create(answers)
            return Response(status=status.HTTP_201_CREATED)
        # Otherwise bulk update existing answers with PUT
        else:
            answer_data = {a["id"]: a["answer"] for a in serializer.data}
            answers = {
                a.id: a for a in Answer.objects.filter(id__in=answer_data.keys())
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
