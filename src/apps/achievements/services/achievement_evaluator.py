"""
AchievementEvaluator - Evaluates if a user meets achievement criteria.
"""

import logging
from decimal import Decimal

from apps.achievements.models import Achievement, UserStatistics
from apps.achievements.services.validators.base import CriteriaValidator
from apps.achievements.services.validators.level_validator import LevelValidator
from apps.achievements.services.validators.streak_validator import StreakValidator
from apps.achievements.services.validators.task_count_validator import TaskCountValidator


logger = logging.getLogger(__name__)


class AchievementEvaluator:
    """
    Evaluates achievement criteria and calculates progress.

    Uses Strategy pattern with different validators for each criteria type.
    """

    def __init__(self):
        self.validators: dict[str, CriteriaValidator] = {
            Achievement.CriteriaType.TASK_COUNT: TaskCountValidator(),
            Achievement.CriteriaType.STREAK: StreakValidator(),
            Achievement.CriteriaType.LEVEL: LevelValidator(),
            # Add more validators as needed
        }

    def evaluate_criteria(
        self,
        user_id: int,
        achievement: Achievement,
        user_stats: UserStatistics,
    ) -> bool:
        """
        Evaluate if user meets achievement criteria.

        Args:
            user_id: User ID
            achievement: Achievement to evaluate
            user_stats: User statistics

        Returns:
            True if criteria are met, False otherwise
        """
        validator = self._get_criteria_validator(achievement.criteria_type)

        if not validator:
            logger.warning(f"No validator found for criteria type: {achievement.criteria_type}")
            return False

        try:
            result = validator.validate(user_stats, achievement.criteria)
            logger.debug(
                f"Criteria evaluation for achievement {achievement.name} (user {user_id}): {result}",
            )
            return result
        except Exception as e:
            logger.error(f"Error evaluating criteria for achievement {achievement.id}: {e}")
            return False

    def calculate_progress(
        self,
        user_id: int,
        achievement: Achievement,
        user_stats: UserStatistics,
    ) -> Decimal:
        """
        Calculate progress percentage for an achievement.

        Args:
            user_id: User ID
            achievement: Achievement to calculate progress for
            user_stats: User statistics

        Returns:
            Progress as Decimal (0.00 to 100.00)
        """
        validator = self._get_criteria_validator(achievement.criteria_type)

        if not validator:
            logger.warning(f"No validator found for criteria type: {achievement.criteria_type}")
            return Decimal("0.00")

        try:
            progress = validator.calculate_progress(user_stats, achievement.criteria)
            # Ensure progress is between 0 and 100
            progress = max(Decimal("0.00"), min(Decimal("100.00"), progress))
            logger.debug(
                f"Progress for achievement {achievement.name} (user {user_id}): {progress}%",
            )
            return progress
        except Exception as e:
            logger.error(f"Error calculating progress for achievement {achievement.id}: {e}")
            return Decimal("0.00")

    def get_user_statistics(self, user_id: int) -> dict:
        """
        Get user statistics as dictionary.

        Args:
            user_id: User ID

        Returns:
            Dictionary with user statistics
        """
        try:
            stats = UserStatistics.objects.get(user_id=user_id)
            return {
                "total_tasks_completed": stats.total_tasks_completed,
                "current_streak": stats.current_streak,
                "longest_streak": stats.longest_streak,
                "total_xp": stats.total_xp,
                "current_level": stats.current_level,
                "friend_count": stats.friend_count,
                "challenges_won": stats.challenges_won,
            }
        except UserStatistics.DoesNotExist:
            logger.warning(f"Statistics not found for user {user_id}")
            return {}

    def _get_criteria_validator(self, criteria_type: str) -> CriteriaValidator:
        """Get appropriate validator for criteria type."""
        return self.validators.get(criteria_type)
