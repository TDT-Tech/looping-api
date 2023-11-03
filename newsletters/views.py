from rest_framework import permissions, viewsets

from newsletters.models import Answer, Newsletter, Question
from newsletters.serializers import (
    AnswerSerializer,
    NewsletterSerializer,
    QuestionSerializer,
)


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
