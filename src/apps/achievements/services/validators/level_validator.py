"""Validator for level criteria."""

from decimal import Decimal

from apps.achievements.models import UserStatistics
from apps.achievements.services.validators.base import CriteriaValidator


class LevelValidator(CriteriaValidator):
    """
    Validates criteria based on user level.

    Expected criteria format:
    {
        "required_level": 10  # Minimum level required
    }
    """

    def validate(self, user_stats: UserStatistics, criteria: dict) -> bool:
        """
        Check if user has reached required level.

        Args:
            user_stats: User statistics
            criteria: Criteria with 'required_level'

        Returns:
            True if current_level >= required_level
        """
        required_level = criteria.get("required_level", 0)
        return user_stats.current_level >= required_level

    def calculate_progress(self, user_stats: UserStatistics, criteria: dict) -> Decimal:
        """
        Calculate progress based on current level.

        Args:
            user_stats: User statistics
            criteria: Criteria with 'required_level'

        Returns:
            Progress percentage as Decimal
        """
        required_level = criteria.get("required_level", 1)
        if required_level == 0:
            return Decimal("100.00")

        current_level = user_stats.current_level
        progress = (Decimal(current_level) / Decimal(required_level)) * Decimal(100)

        return min(progress, Decimal("100.00"))
