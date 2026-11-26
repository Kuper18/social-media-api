from django.urls import include, path
from rest_framework import routers

from user_profile.views import ProfileViewSet

router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)

urlpatterns = (path("", include(router.urls)),)

app_name = "user_profile"
