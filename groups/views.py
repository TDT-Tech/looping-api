from rest_framework import permissions, viewsets

from groups.models import Group
from groups.serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
