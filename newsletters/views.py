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

    @action(detail=True, methods=["GET", "POST", "PUT"])
    def answers(self, request, pk=None):
        newsletter = self.get_object()
        if request.method == "GET":
            answers = Answer.objects.filter(newsletter_id=newsletter.id)
            serializer = AnswerSerializer(answers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method in ["POST", "PUT"]:
            data = request.data
            serializer = (
                AnswerCreateSerializer(data=data, many=True)
                if request.method == "POST"
                else AnswerSerializer(data=data, many=True)
            )
            if not serializer.is_valid():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if request.method == "PUT":
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

            answers = []
            submitter = request.user.name
            for answer in serializer.data:
                new_answer = Answer(
                    question_id=answer["question_id"],
                    answer=answer["answer"],
                    submitter=submitter,
                    newsletter_id=newsletter.id,
                )
                answers.append(new_answer)
            Answer.objects.bulk_create(answers)
            return Response(status=status.HTTP_201_CREATED)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
