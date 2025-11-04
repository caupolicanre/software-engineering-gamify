"""AchievementService - Main business logic for achievement operations."""

import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from apps.achievements.events.publishers import EventPublisher
from apps.achievements.models import Achievement, UserAchievement, UserStatistics
from apps.achievements.services.achievement_evaluator import AchievementEvaluator
from apps.achievements.utils.notification_sender import NotificationSender
from apps.achievements.utils.validators import AchievementValidator


User = get_user_model()
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

    def __init__(self) -> None:
        """Initialize the AchievementService."""
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
        logger.info("Checking achievements for user %s after event %s (event_data: %s)", user_id, event_type, event_data)

        # Get user statistics
        try:
            user_stats = UserStatistics.objects.get(user_id=user_id)
        except UserStatistics.DoesNotExist:
            logger.warning("User statistics not found for user %s. Creating default", user_id)
            user = User.objects.get(id=user_id)
            user_stats = UserStatistics.objects.create(user=user)

        # Get relevant achievements based on event type
        achievements = self._get_relevant_achievements(event_type)

        newly_unlocked = []

        for achievement in achievements:
            # Check if already unlocked
            if not self.validator.validate_not_already_unlocked(user_id, achievement.id):
                logger.debug("Achievement %s already unlocked for user %s", achievement.id, user_id)
                continue

            # Evaluate criteria
            logger.debug("Evaluating achievement %s (%s) for user %s", achievement.name, achievement.id, user_id)
            criteria_met = self.evaluator.evaluate_criteria(
                user_id,
                achievement,
                user_stats,
            )

            logger.debug("Criteria met for achievement %s: %s", achievement.name, criteria_met)

            if criteria_met:
                # Unlock achievement
                logger.info("Unlocking achievement %s for user %s", achievement.name, user_id)
                user_achievement = self.unlock_achievement(user_id, achievement.id)
                newly_unlocked.append(user_achievement)
            else:
                # Update progress
                progress = self.evaluator.calculate_progress(
                    user_id,
                    achievement,
                    user_stats,
                )
                logger.debug("Updating progress for achievement %s: %s%%", achievement.name, progress)
                self._update_progress(user_id, achievement.id, progress)

        logger.info("Unlocked %d achievements for user %s", len(newly_unlocked), user_id)
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
        logger.info("Unlocking achievement %s for user %s", achievement_id, user_id)

        # Validate user exists
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist as exc:
            msg = f"User {user_id} does not exist"
            raise ValueError(msg) from exc

        # Validate achievement
        if not self.validator.validate_achievement_exists(achievement_id):
            msg = f"Achievement {achievement_id} does not exist"
            raise ValueError(msg)

        if not self.validator.validate_not_already_unlocked(user_id, achievement_id):
            msg = f"Achievement {achievement_id} already unlocked for user {user_id}"
            raise ValueError(msg)

        # Get achievement
        achievement = Achievement.objects.get(id=achievement_id)

        # Create or update user achievement
        user_achievement, created = UserAchievement.objects.get_or_create(
            user=user,
            achievement=achievement,
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

        logger.info("Achievement %s unlocked for user %s", achievement.name, user_id)
        return user_achievement

    def get_user_achievements(
        self,
        user_id: int,
        *,
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
            List of progress dictionaries with full achievement details

        """
        try:
            user_stats = UserStatistics.objects.get(user_id=user_id)
        except UserStatistics.DoesNotExist:
            # Get User instance and create statistics
            user = User.objects.get(id=user_id)
            user_stats = UserStatistics.objects.create(user=user)

        achievements = Achievement.objects.get_active_achievements()

        # Get all user achievements to check unlock status
        user_achievements = {ua.achievement_id: ua for ua in UserAchievement.objects.filter(user_id=user_id)}

        result = []

        for achievement in achievements:
            # Check if unlocked
            user_achievement = user_achievements.get(achievement.id)
            is_unlocked = user_achievement.is_completed if user_achievement else False
            unlocked_at = user_achievement.unlocked_at if user_achievement and user_achievement.unlocked_at else None

            # Get current and target values based on criteria type
            current_value, target_value = self._get_progress_values(achievement, user_stats)

            if is_unlocked:
                progress_percentage = 100.0
                current_value = target_value
            else:
                progress_percentage = self.evaluator.calculate_progress(user_id, achievement, user_stats)

            # Ensure criteria has target field for frontend
            criteria = achievement.criteria.copy() if achievement.criteria else {}
            if "target" not in criteria:
                criteria["target"] = target_value

            result.append(
                {
                    "id": str(achievement.id),
                    "name": achievement.name,
                    "description": achievement.description,
                    "criteria": criteria,
                    "criteria_type": achievement.criteria_type,
                    "reward_xp": achievement.reward_xp,
                    "reward_coins": achievement.reward_coins,
                    "icon": achievement.icon,
                    "rarity": achievement.rarity,
                    "progress": current_value,
                    "progress_percentage": float(progress_percentage),
                    "is_unlocked": is_unlocked,
                    "unlocked_at": unlocked_at.isoformat() if unlocked_at else None,
                },
            )

        return result

    def _get_progress_values(self, achievement: Achievement, user_stats: UserStatistics) -> tuple[int, int]:
        """
        Extract current and target values based on criteria type.

        Args:
            achievement: Achievement instance
            user_stats: User statistics

        Returns:
            Tuple of (current_value, target_value)
        """
        criteria = achievement.criteria or {}
        criteria_type = achievement.criteria_type

        if criteria_type == Achievement.CriteriaType.TASK_COUNT:
            return user_stats.total_tasks_completed, criteria.get("required_count", 0)
        if criteria_type == Achievement.CriteriaType.STREAK:
            return user_stats.current_streak, criteria.get("required_days", 0)
        if criteria_type == Achievement.CriteriaType.LEVEL:
            return user_stats.current_level, criteria.get("required_level", 0)
        if criteria_type == Achievement.CriteriaType.FRIEND_COUNT:
            return user_stats.friend_count, criteria.get("required_count", 0)
        if criteria_type == Achievement.CriteriaType.CHALLENGE:
            return user_stats.challenges_won, criteria.get("required_wins", 0)
        return 0, 100

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

    def _update_progress(self, user_id: int, achievement_id: str, progress: float) -> None:
        """Update progress for an achievement."""
        user_achievement, _created = UserAchievement.objects.get_or_create_progress(
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

        logger.info("Granted rewards to user %s: %s", user_id, rewards)
        # NOTE: External Reward Service integration pending

        return rewards

    def _publish_achievement_event(
        self,
        user_id: int,
        achievement: Achievement,
        rewards: dict,
    ) -> None:
        """Publish AchievementUnlocked event."""
        self.event_publisher.publish_achievement_unlocked(
            user_id=user_id,
            achievement_id=str(achievement.id),
            achievement_name=achievement.name,
            rewards=rewards,
        )

    def _notify_achievement_unlock(self, user_id: int, achievement: Achievement) -> None:
        """Send notification about achievement unlock."""
        self.notification_sender.send_achievement_notification(
            user_id=user_id,
            achievement_name=achievement.name,
            description=achievement.description,
        )
