"""
URL configuration for Achievement API.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.achievements.api.viewsets import AchievementViewSet


app_name = "achievements"

router = DefaultRouter()
router.register(r"achievements", AchievementViewSet, basename="achievement")

urlpatterns = [
    path("", include(router.urls)),
]
