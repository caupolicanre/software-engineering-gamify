"""Validator for task count criteria."""

from decimal import Decimal

from apps.achievements.models import UserStatistics
from apps.achievements.services.validators.base import CriteriaValidator


class TaskCountValidator(CriteriaValidator):
    """
    Validates criteria based on number of completed tasks.

    Expected criteria format:
    {
        "required_count": 10,  # Number of tasks required
        "type": "total"        # Optional: "total" or "consecutive_days"
    }
    """

    def validate(self, user_stats: UserStatistics, criteria: dict) -> bool:
        """
        Check if user has completed required number of tasks.

        Args:
            user_stats: User statistics
            criteria: Criteria with 'required_count'

        Returns:
            True if user has completed >= required_count tasks
        """
        required_count = criteria.get("required_count", 0)
        return user_stats.total_tasks_completed >= required_count

    def calculate_progress(self, user_stats: UserStatistics, criteria: dict) -> Decimal:
        """
        Calculate progress based on completed tasks.

        Args:
            user_stats: User statistics
            criteria: Criteria with 'required_count'

        Returns:
            Progress percentage as Decimal
        """
        required_count = criteria.get("required_count", 1)
        if required_count == 0:
            return Decimal("100.00")

        current_count = user_stats.total_tasks_completed
        progress = (Decimal(current_count) / Decimal(required_count)) * Decimal(100)

        return min(progress, Decimal("100.00"))
