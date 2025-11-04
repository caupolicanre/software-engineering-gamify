"""ViewSets for Achievement API endpoints."""

import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from apps.achievements.models import Achievement
from apps.achievements.serializers import (
    AchievementProgressSerializer,
    AchievementSerializer,
    AchievementUnlockRequestSerializer,
    UserAchievementListSerializer,
    UserAchievementSerializer,
)
from apps.achievements.services.achievement_service import AchievementService


logger = logging.getLogger(__name__)


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Achievement CRUD operations.

    Endpoints:
        GET    /achievements/               - List all achievements
        GET    /achievements/{id}/          - Get achievement detail
        GET    /achievements/me/            - Get current user's achievements
        GET    /achievements/available/     - Get available achievements
        GET    /achievements/{id}/progress/ - Check progress for achievement
        POST   /achievements/unlock/        - Manually unlock achievement (dev/testing)
        GET    /achievements/all-progress/  - Get all progress for user
    """

    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["rarity", "criteria_type", "is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "reward_xp", "reward_coins"]
    ordering = ["-created_at"]

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the viewset."""
        super().__init__(*args, **kwargs)
        self.achievement_service = AchievementService()

    def get_queryset(self):
        """Get queryset - only active achievements for non-staff."""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    @action(detail=False, methods=["get"], url_path="me")
    def get_user_achievements(self, request):
        """
        Get all achievements for the authenticated user.

        Query params:
            - include_locked: bool (default: False) - Include locked achievements

        Returns:
            List of user achievements with progress
        """
        user_id = request.user.id
        include_locked = request.query_params.get("include_locked", "false").lower() == "true"

        try:
            achievements = self.achievement_service.get_user_achievements(
                user_id=user_id,
                include_locked=include_locked,
            )

            serializer = UserAchievementListSerializer(achievements, many=True)
            return Response(serializer.data)

        except Exception:
            logger.exception("Error getting user achievements")
            return Response(
                {"error": "Failed to retrieve achievements"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def available(self, request) -> Response:
        """
        Get all available (active) achievements.

        Returns:
            List of active achievements
        """
        achievements = Achievement.objects.get_active_achievements()
        serializer = self.get_serializer(achievements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def progress(self, request, pk=None) -> Response:
        """
        Check progress for a specific achievement.

        Args:
            pk: Achievement ID

        Returns:
            Progress information for the achievement
        """
        user_id = request.user.id
        achievement_id = pk

        try:
            progress_data = self.achievement_service.get_achievement_progress(
                user_id=user_id,
                achievement_id=achievement_id,
            )

            serializer = AchievementProgressSerializer(data=progress_data)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data)

        except Achievement.DoesNotExist:
            return Response(
                {"error": "Achievement not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            logger.exception("Error checking achievement progress")
            return Response(
                {"error": "Failed to check progress"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"])
    def unlock(self, request) -> Response:
        """
        Manually unlock an achievement (for testing/dev purposes).

        Request body:
            {
                "achievement_id": "uuid"
            }

        Returns:
            Unlocked user achievement
        """
        serializer = AchievementUnlockRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = request.user.id
        achievement_id = serializer.validated_data["achievement_id"]

        try:
            user_achievement = self.achievement_service.unlock_achievement(
                user_id=user_id,
                achievement_id=str(achievement_id),
            )

            response_serializer = UserAchievementSerializer(user_achievement)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            logger.exception("Error unlocking achievement")
            return Response(
                {"error": "Failed to unlock achievement"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"], url_path="all-progress")
    def get_all_progress(self, request) -> Response:
        """
        Get progress for all achievements for the authenticated user.

        Returns:
            List of progress data for all achievements
        """
        user_id = request.user.id

        try:
            progress_list = self.achievement_service.calculate_all_progress(user_id)
            return Response(progress_list)

        except Exception:
            logger.exception("Error calculating all progress")
            return Response(
                {"error": "Failed to calculate progress"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
