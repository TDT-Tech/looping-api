from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from groups.models import Group
from groups.permissions import AdminAllButMemberReadOnly
from groups.serializers import GroupSerializer
from newsletters.models import Question
from newsletters.serializers import QuestionSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AdminAllButMemberReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(users=self.request.user)

    @action(detail=True, methods=["GET"])
    def questions(self, request, pk=None):
        group = self.get_object()
        questions = Question.objects.filter(group_id=group.id)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    @action(
        detail=True, methods=["DELETE"], url_path="questions/(?P<question_pk>[^/.]+)"
    )
    def remove_question(self, request, question_pk, pk=None):
        group = self.get_object()
        Question.objects.filter(group_id=group.id, id=question_pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
