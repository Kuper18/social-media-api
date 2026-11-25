from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user_profile.filters import ProfileFilter
from user_profile.models import Follower, Profile
from user_profile.paginations import PageNumberPagination
from user_profile.permissions import IsOwnerOrReadOnly
from user_profile.serializers import (
    AvatarSerializer,
    ProfileRetrieveSerializer,
    ProfileSerializer,
)
from user_profile.serializers.follower import FollowSerializer
from user_profile.serializers.profile import ProfileListSerializer


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
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = ProfileFilter
    search_fields = ("nickname",)

    def get_permissions(self):
        if self.action in ("follow", "list", "retrieve"):
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "upload_avatar":
            return AvatarSerializer

        if self.action == "retrieve":
            return ProfileRetrieveSerializer

        if self.action == "follow":
            return FollowSerializer

        if self.action in ("list", "following", "followers"):
            return ProfileListSerializer

        return ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def _get_paginated_profiles(self, profiles: QuerySet) -> Response:
        page = self.paginate_queryset(profiles)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["POST"], url_path="upload-avatar")
    def upload_avatar(self, request: Request, pk=None) -> Response:
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST", "DELETE"], url_path="follow")
    def follow(self, request: Request, pk=None) -> Response:

        following_profile = self.get_object()

        if request.method == "POST":
            serializer = self.get_serializer(
                data={
                    "follower": request.user.id,
                    "following": following_profile.user.id,
                },
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {"detail": "You are following this user."},
                status=status.HTTP_201_CREATED,
            )

        is_deleted, _ = Follower.objects.filter(
            follower=request.user.id, following=following_profile.user.id
        ).delete()

        if not is_deleted:
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=True, methods=["GET"], url_path="followers")
    def followers(self, request: Request, pk=None) -> Response:
        profile = self.get_object()
        followers = Profile.objects.filter(
            user__following__following=profile.user.id
        )
        return self._get_paginated_profiles(followers)

    @action(detail=True, methods=["GET"], url_path="following")
    def following(self, request: Request, pk=None) -> Response:
        profile = self.get_object()
        following = Profile.objects.filter(
            user__followers__follower=profile.user.id
        )
        return self._get_paginated_profiles(following)
