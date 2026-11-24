from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from follower.models import Follower
from user_profile.models import Profile


class FollowerViewSet(GenericViewSet):
    queryset = Follower.objects.all()

    @staticmethod
    def _validate(
        follower: AbstractBaseUser | AnonymousUser, following: AbstractBaseUser
    ) -> Response | None:
        if follower == following:
            return Response(
                {"detail": "You cannot perform this action."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return None

    @staticmethod
    def _get_object_profile(pk: int | None) -> Profile:
        return get_object_or_404(
            Profile.objects.select_related("user"),
            pk=pk,
        )

    @action(detail=True, methods=["POST"])
    def follow(self, request: Request, pk=None) -> Response:
        follower = request.user
        following_profile = self._get_object_profile(pk)
        following_user = following_profile.user

        self._validate(follower, following_user)

        Follower.objects.create(follower=follower, following=following_user)

        return Response(
            {
                "detail": "You are following current user.",
            },
            status=status.HTTP_201_CREATED,
        )
