"""Validator for streak criteria."""

from decimal import Decimal

from apps.achievements.models import UserStatistics
from apps.achievements.services.validators.base import CriteriaValidator


class StreakValidator(CriteriaValidator):
    """
    Validates criteria based on consecutive days streaks.

    Expected criteria format:
    {
        "required_days": 7,        # Number of consecutive days required
        "type": "consecutive_days" # Type of streak
    }
    """

    def validate(self, user_stats: UserStatistics, criteria: dict) -> bool:
        """
        Check if user has achieved required streak.

        Args:
            user_stats: User statistics
            criteria: Criteria with 'required_days'

        Returns:
            True if current_streak >= required_days
        """
        required_days = criteria.get("required_days", 0)
        return user_stats.current_streak >= required_days

    def calculate_progress(self, user_stats: UserStatistics, criteria: dict) -> Decimal:
        """
        Calculate progress based on current streak.

        Args:
            user_stats: User statistics
            criteria: Criteria with 'required_days'

        Returns:
            Progress percentage as Decimal
        """
        required_days = criteria.get("required_days", 1)
        if required_days == 0:
            return Decimal("100.00")

        current_days = user_stats.current_streak
        progress = (Decimal(current_days) / Decimal(required_days)) * Decimal(100)

        return min(progress, Decimal("100.00"))
