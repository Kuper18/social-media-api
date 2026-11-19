from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user.models import Profile
from user.paginations import PageNumberPagination
from user.permissions import IsOwnerOrReadOnly
from user.serializers import AvatarSerializer, ProfileSerializer


class ProfileViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Profile.objects.select_related("user")
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "upload_avatar":
            return AvatarSerializer

        return ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"], url_path="upload-avatar")
    def upload_avatar(self, request: Request, pk=None) -> Response:
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
