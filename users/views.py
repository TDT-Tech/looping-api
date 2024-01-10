from rest_framework import mixins, viewsets

from users.models import User
from users.permissions import IsOwner
from users.serializers import UserSerializer


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]
