"""Custom manager for Achievement model."""

from django.db import models


class AchievementManager(models.Manager):
    """Custom manager for Achievement model with useful queries."""

    def get_active_achievements(self) -> models.QuerySet:
        """Get all active achievements."""
        return self.filter(is_active=True)

    def get_by_rarity(self, rarity: str) -> models.QuerySet:
        """
        Get achievements by rarity.

        Args:
            rarity: Rarity level (common, rare, epic, legendary)

        Returns:
            QuerySet of achievements

        """
        return self.filter(rarity=rarity, is_active=True)

    def get_by_criteria_type(self, criteria_type: str) -> models.QuerySet:
        """
        Get achievements by criteria type.

        Args:
            criteria_type: Type of criteria (task_count, streak, level, etc.)

        Returns:
            QuerySet of achievements

        """
        return self.filter(criteria_type=criteria_type, is_active=True)

    def search_by_name(self, query: str) -> models.QuerySet:
        """
        Search achievements by name.

        Args:
            query: Search query string

        Returns:
            QuerySet of matching achievements

        """
        return self.filter(name__icontains=query, is_active=True)


class UserAchievementManager(models.Manager):
    """Custom manager for UserAchievement model."""

    def get_user_unlocked(self, user_id: int) -> models.QuerySet:
        """
        Get all unlocked achievements for a user.

        Args:
            user_id: User ID

        Returns:
            QuerySet of unlocked user achievements

        """
        return self.filter(user_id=user_id, is_completed=True).select_related("achievement")

    def get_user_in_progress(self, user_id: int) -> models.QuerySet:
        """
        Get achievements in progress for a user.

        Args:
            user_id: User ID

        Returns:
            QuerySet of in-progress user achievements

        """
        return self.filter(
            user_id=user_id,
            is_completed=False,
            progress__gt=0,
        ).select_related("achievement")

    def is_unlocked(self, user_id: int, achievement_id: int) -> bool:
        """
        Check if a user has unlocked a specific achievement.

        Args:
            user_id: User ID
            achievement_id: Achievement ID

        Returns:
            Boolean indicating if unlocked

        """
        return self.filter(
            user_id=user_id,
            achievement_id=achievement_id,
            is_completed=True,
        ).exists()

    def get_or_create_progress(self, user_id: int, achievement_id: int) -> tuple:
        """
        Get or create a UserAchievement progress record.

        Args:
            user_id: User ID
            achievement_id: Achievement ID

        Returns:
            Tuple (UserAchievement instance, created boolean)

        """
        return self.get_or_create(
            user_id=user_id,
            achievement_id=achievement_id,
            defaults={"progress": 0.00, "is_completed": False},
        )

    def bulk_update_progress(self, user_achievements: list) -> int:
        """
        Bulk update progress for multiple user achievements.

        Args:
            user_achievements: List of UserAchievement instances

        Returns:
            Number of updated records

        """
        return self.bulk_update(
            user_achievements,
            ["progress", "updated_at"],
            batch_size=100,
        )
