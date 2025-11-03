"""
Business validation utilities for achievements.
"""

import logging

from apps.achievements.models import Achievement, UserAchievement


logger = logging.getLogger(__name__)


class AchievementValidator:
    """
    Validates business rules for achievements.
    """

    def validate_achievement_exists(self, achievement_id: str) -> bool:
        """
        Validate that an achievement exists.

        Args:
            achievement_id: Achievement UUID

        Returns:
            True if achievement exists
        """
        return Achievement.objects.filter(id=achievement_id).exists()

    def validate_not_already_unlocked(self, user_id: int, achievement_id: str) -> bool:
        """
        Validate that achievement is not already unlocked by user.

        Args:
            user_id: User ID
            achievement_id: Achievement UUID

        Returns:
            True if NOT already unlocked (can be unlocked)
        """
        return not UserAchievement.objects.filter(
            user_id=user_id,
            achievement_id=achievement_id,
            is_completed=True,
        ).exists()

    def validate_criteria_format(self, criteria: dict) -> bool:
        """
        Validate criteria JSON format.

        Args:
            criteria: Criteria dictionary

        Returns:
            True if format is valid
        """
        if not isinstance(criteria, dict):
            logger.warning("Criteria must be a dictionary")
            return False

        # Check for required keys based on type
        # This is a basic validation
        return True

    def validate_user_eligible(self, user_id: int, achievement_id: str) -> bool:
        """
        Validate that user is eligible to unlock achievement.

        Args:
            user_id: User ID
            achievement_id: Achievement UUID

        Returns:
            True if user is eligible
        """
        # Check if achievement exists and is active
        try:
            achievement = Achievement.objects.get(id=achievement_id)
            if not achievement.is_active:
                logger.warning(f"Achievement {achievement_id} is not active")
                return False
        except Achievement.DoesNotExist:
            logger.warning(f"Achievement {achievement_id} does not exist")
            return False

        # Check if not already unlocked
        if not self.validate_not_already_unlocked(user_id, achievement_id):
            logger.warning(f"Achievement {achievement_id} already unlocked for user {user_id}")
            return False

        return True

    def validate_reward_values(self, xp: int, coins: int) -> bool:
        """
        Validate reward values are positive.

        Args:
            xp: XP reward
            coins: Coins reward

        Returns:
            True if valid
        """
        if xp < 0 or coins < 0:
            logger.warning(f"Reward values must be positive: xp={xp}, coins={coins}")
            return False
        return True
