"""Base abstract class for criteria validators."""

from abc import ABC, abstractmethod
from decimal import Decimal

from apps.achievements.models import UserStatistics


class CriteriaValidator(ABC):
    """
    Abstract base class for achievement criteria validators.

    Each criteria type (task_count, streak, level, etc.)
    should have its own validator implementation.
    """

    @abstractmethod
    def validate(self, user_stats: UserStatistics, criteria: dict) -> bool:
        """
        Validate if user meets the criteria.

        Args:
            user_stats: User statistics
            criteria: Criteria configuration from Achievement.criteria JSON field

        Returns:
            True if criteria are met, False otherwise
        """

    @abstractmethod
    def calculate_progress(self, user_stats: UserStatistics, criteria: dict) -> Decimal:
        """
        Calculate progress percentage towards meeting criteria.

        Args:
            user_stats: User statistics
            criteria: Criteria configuration

        Returns:
            Progress as Decimal (0.00 to 100.00)
        """
