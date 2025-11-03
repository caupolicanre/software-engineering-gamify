"""
AchievementService - Main business logic for achievement operations.
"""

import logging

from django.db import transaction
from django.utils import timezone

from apps.achievements.events.publishers import EventPublisher
from apps.achievements.models import Achievement, UserAchievement, UserStatistics
from apps.achievements.services.achievement_evaluator import AchievementEvaluator
from apps.achievements.utils.notification_sender import NotificationSender
from apps.achievements.utils.validators import AchievementValidator


logger = logging.getLogger(__name__)


class AchievementService:
    """
    Orchestrates all achievement-related business logic.

    Responsibilities:
        - Check and unlock achievements
        - Calculate progress
        - Grant rewards
        - Publish events
        - Send notifications
    """

    def __init__(self):
        self.evaluator = AchievementEvaluator()
        self.validator = AchievementValidator()
        self.event_publisher = EventPublisher()
        self.notification_sender = NotificationSender()

    @transaction.atomic
    def check_and_unlock_achievements(
        self,
        user_id: int,
        event_type: str,
        event_data: dict,
    ) -> list[UserAchievement]:
        """
        Check all achievements and unlock those whose criteria are met.

        Args:
            user_id: User ID
            event_type: Type of event that triggered this check (e.g., 'task_completed')
            event_data: Event data containing relevant information

        Returns:
            List of newly unlocked UserAchievement instances

        """
        logger.info(f"Checking achievements for user {user_id} after event {event_type}")

        # Get user statistics
        try:
            user_stats = UserStatistics.objects.get(user_id=user_id)
        except UserStatistics.DoesNotExist:
            logger.warning(f"User statistics not found for user {user_id}. Creating default.")
            user_stats = UserStatistics.objects.create(user_id=user_id)

        # Get relevant achievements based on event type
        achievements = self._get_relevant_achievements(event_type)

        newly_unlocked = []

        for achievement in achievements:
            # Check if already unlocked
            if not self.validator.validate_not_already_unlocked(user_id, achievement.id):
                logger.debug(f"Achievement {achievement.id} already unlocked for user {user_id}")
                continue

            # Evaluate criteria
            criteria_met = self.evaluator.evaluate_criteria(
                user_id,
                achievement,
                user_stats,
            )

            if criteria_met:
                # Unlock achievement
                user_achievement = self.unlock_achievement(user_id, achievement.id)
                newly_unlocked.append(user_achievement)
            else:
                # Update progress
                progress = self.evaluator.calculate_progress(
                    user_id,
                    achievement,
                    user_stats,
                )
                self._update_progress(user_id, achievement.id, progress)

        logger.info(f"Unlocked {len(newly_unlocked)} achievements for user {user_id}")
        return newly_unlocked

    @transaction.atomic
    def unlock_achievement(
        self,
        user_id: int,
        achievement_id: str,
    ) -> UserAchievement:
        """
        Unlock a specific achievement for a user.

        Args:
            user_id: User ID
            achievement_id: Achievement UUID

        Returns:
            UserAchievement instance

        Raises:
            ValueError: If achievement doesn't exist or is already unlocked

        """
        logger.info(f"Unlocking achievement {achievement_id} for user {user_id}")

        # Validate
        if not self.validator.validate_achievement_exists(achievement_id):
            raise ValueError(f"Achievement {achievement_id} does not exist")

        if not self.validator.validate_not_already_unlocked(user_id, achievement_id):
            raise ValueError(f"Achievement {achievement_id} already unlocked for user {user_id}")

        # Get achievement
        achievement = Achievement.objects.get(id=achievement_id)

        # Create or update user achievement
        user_achievement, created = UserAchievement.objects.get_or_create(
            user_id=user_id,
            achievement_id=achievement_id,
            defaults={
                "progress": 100.00,
                "is_completed": True,
                "unlocked_at": timezone.now(),
            },
        )

        if not created:
            user_achievement.complete()

        # Grant rewards
        rewards = self._grant_achievement_rewards(user_id, achievement)

        # Publish event
        self._publish_achievement_event(user_id, achievement, rewards)

        # Send notification
        self._notify_achievement_unlock(user_id, achievement)

        logger.info(f"Achievement {achievement.name} unlocked for user {user_id}")
        return user_achievement

    def get_user_achievements(
        self,
        user_id: int,
        include_locked: bool = False,
    ) -> list[dict]:
        """
        Get all achievements for a user.

        Args:
            user_id: User ID
            include_locked: Whether to include locked achievements

        Returns:
            List of achievement dictionaries with progress

        """
        if include_locked:
            achievements = Achievement.objects.get_active_achievements()
            user_achievements = UserAchievement.objects.filter(user_id=user_id)

            # Map user achievements
            user_ach_map = {ua.achievement_id: ua for ua in user_achievements}

            result = []
            for ach in achievements:
                user_ach = user_ach_map.get(ach.id)
                result.append(
                    {
                        "achievement": ach,
                        "progress": float(user_ach.progress) if user_ach else 0.0,
                        "is_unlocked": user_ach.is_completed if user_ach else False,
                        "unlocked_at": user_ach.unlocked_at if user_ach else None,
                    },
                )
            return result
        user_achievements = UserAchievement.objects.get_user_unlocked(user_id)
        return [
            {
                "achievement": ua.achievement,
                "progress": float(ua.progress),
                "is_unlocked": True,
                "unlocked_at": ua.unlocked_at,
            }
            for ua in user_achievements
        ]

    def get_achievement_progress(
        self,
        user_id: int,
        achievement_id: str,
    ) -> dict:
        """
        Get progress for a specific achievement.

        Args:
            user_id: User ID
            achievement_id: Achievement UUID

        Returns:
            Dictionary with progress information

        """
        achievement = Achievement.objects.get(id=achievement_id)

        try:
            user_achievement = UserAchievement.objects.get(
                user_id=user_id,
                achievement_id=achievement_id,
            )
            current_progress = float(user_achievement.progress)
            is_unlocked = user_achievement.is_completed
        except UserAchievement.DoesNotExist:
            current_progress = 0.0
            is_unlocked = False

        # Calculate required progress from criteria
        required_progress = achievement.criteria.get("required_count", 100)

        return {
            "achievement_id": str(achievement.id),
            "achievement_name": achievement.name,
            "current_progress": current_progress,
            "required_progress": required_progress,
            "percentage": current_progress,
            "is_unlocked": is_unlocked,
        }

    def calculate_all_progress(self, user_id: int) -> list[dict]:
        """
        Calculate progress for all achievements for a user.

        Args:
            user_id: User ID

        Returns:
            List of progress dictionaries

        """
        try:
            user_stats = UserStatistics.objects.get(user_id=user_id)
        except UserStatistics.DoesNotExist:
            user_stats = UserStatistics.objects.create(user_id=user_id)

        achievements = Achievement.objects.get_active_achievements()
        result = []

        for achievement in achievements:
            progress = self.evaluator.calculate_progress(user_id, achievement, user_stats)
            result.append(
                {
                    "achievement_id": str(achievement.id),
                    "achievement_name": achievement.name,
                    "progress_percentage": float(progress),
                    "criteria_type": achievement.criteria_type,
                },
            )

        return result

    # Private helper methods

    def _get_relevant_achievements(self, event_type: str) -> list[Achievement]:
        """Get achievements relevant to the event type."""
        criteria_type_map = {
            "task_completed": Achievement.CriteriaType.TASK_COUNT,
            "streak_milestone": Achievement.CriteriaType.STREAK,
            "level_up": Achievement.CriteriaType.LEVEL,
            "friend_added": Achievement.CriteriaType.FRIEND_COUNT,
            "challenge_won": Achievement.CriteriaType.CHALLENGE,
        }

        criteria_type = criteria_type_map.get(event_type)
        if criteria_type:
            return list(Achievement.objects.get_by_criteria_type(criteria_type))

        return list(Achievement.objects.get_active_achievements())

    def _update_progress(self, user_id: int, achievement_id: str, progress: float):
        """Update progress for an achievement."""
        user_achievement, created = UserAchievement.objects.get_or_create_progress(
            user_id,
            achievement_id,
        )
        user_achievement.update_progress(progress)

    def _grant_achievement_rewards(self, user_id: int, achievement: Achievement) -> dict:
        """Grant rewards for unlocking achievement."""
        # This would call RewardService in a real implementation
        rewards = {
            "xp": achievement.reward_xp,
            "coins": achievement.reward_coins,
        }

        logger.info(f"Granted rewards to user {user_id}: {rewards}")
        # TODO: Call external Reward Service

        return rewards

    def _publish_achievement_event(self, user_id: int, achievement: Achievement, rewards: dict):
        """Publish AchievementUnlocked event."""
        self.event_publisher.publish_achievement_unlocked(
            user_id=user_id,
            achievement_id=str(achievement.id),
            achievement_name=achievement.name,
            rewards=rewards,
        )

    def _notify_achievement_unlock(self, user_id: int, achievement: Achievement):
        """Send notification about achievement unlock."""
        self.notification_sender.send_achievement_notification(
            user_id=user_id,
            achievement_name=achievement.name,
            description=achievement.description,
        )
