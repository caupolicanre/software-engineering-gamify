"""URL configuration for Achievement API."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


app_name = "achievements"

router = DefaultRouter()
router.register(r"achievements", views.AchievementViewSet, basename="achievement")

urlpatterns = [
    path("", include(router.urls)),
]
