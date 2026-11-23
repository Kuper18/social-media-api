from django.urls import include
from rest_framework import routers

from follower.views import FollowerViewSet

router = routers.DefaultRouter()
router.register("followers", FollowerViewSet)

urlpatterns = (include(router.urls),)

app_name = "follower"
