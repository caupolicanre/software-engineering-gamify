"""Event handlers that listen to external events and trigger achievement checks."""

import logging

from apps.achievements.services.achievement_service import AchievementService


logger = logging.getLogger(__name__)


class TaskCompletedEventHandler:
    """
    Handles TaskCompleted events from Task Service.

    When a task is completed, checks if any task-related achievements
    should be unlocked.
    """

    def __init__(self) -> None:
        """Initialize the TaskCompletedEventHandler."""
        self.achievement_service = AchievementService()

    def handle_task_completed(self, event_data: dict) -> None:
        """
        Process TaskCompleted event.

        Args:
            event_data: Event payload with task information
                {
                    'user_id': int,
                    'task_id': str,
                    'difficulty': str,
                    'timestamp': str,
                    'xp_earned': int
                }
        """
        try:
            user_id = self._extract_user_id(event_data)
            task_info = self._extract_task_info(event_data)

            logger.info("Handling TaskCompleted event for user %s", user_id)

            # Check and unlock achievements
            unlocked = self.achievement_service.check_and_unlock_achievements(
                user_id=user_id,
                event_type="task_completed",
                event_data=task_info,
            )

            logger.info("Unlocked %d achievements for user %s", len(unlocked), user_id)

        except Exception:
            logger.exception("Error handling TaskCompleted event")

    def _extract_user_id(self, event_data: dict) -> int:
        """Extract user_id from event data."""
        return event_data.get("user_id")

    def _extract_task_info(self, event_data: dict) -> dict:
        """Extract task information from event data."""
        return {
            "task_id": event_data.get("task_id"),
            "difficulty": event_data.get("difficulty"),
            "timestamp": event_data.get("timestamp"),
            "xp_earned": event_data.get("xp_earned", 0),
        }


class StreakMilestoneEventHandler:
    """
    Handles StreakMilestone events.

    When a user reaches a streak milestone, checks for streak-related achievements.
    """

    def __init__(self) -> None:
        """Initialize the StreakMilestoneEventHandler."""
        self.achievement_service = AchievementService()

    def handle_streak_milestone(self, event_data: dict) -> None:
        """
        Process StreakMilestone event.

        Args:
            event_data: Event payload
                {
                    'user_id': int,
                    'streak_days': int,
                    'timestamp': str
                }
        """
        try:
            user_id = event_data.get("user_id")
            streak_days = self._extract_streak_days(event_data)

            logger.info("Handling StreakMilestone event for user %s (%d days)", user_id, streak_days)

            # Check and unlock achievements
            unlocked = self.achievement_service.check_and_unlock_achievements(
                user_id=user_id,
                event_type="streak_milestone",
                event_data={"streak_days": streak_days},
            )

            logger.info("Unlocked %d streak achievements for user %s", len(unlocked), user_id)

        except Exception:
            logger.exception("Error handling StreakMilestone event")

    def _extract_streak_days(self, event_data: dict) -> int:
        """Extract streak days from event data."""
        return event_data.get("streak_days", 0)


class LevelUpEventHandler:
    """
    Handles LevelUp events.

    When a user levels up, checks for level-related achievements.
    """

    def __init__(self) -> None:
        """Initialize the LevelUpEventHandler."""
        self.achievement_service = AchievementService()

    def handle_level_up(self, event_data: dict) -> None:
        """
        Process LevelUp event.

        Args:
            event_data: Event payload
                {
                    'user_id': int,
                    'old_level': int,
                    'new_level': int,
                    'timestamp': str
                }
        """
        try:
            user_id = event_data.get("user_id")
            new_level = self._extract_new_level(event_data)

            logger.info("Handling LevelUp event for user %s (level %d)", user_id, new_level)

            # Check and unlock achievements
            unlocked = self.achievement_service.check_and_unlock_achievements(
                user_id=user_id,
                event_type="level_up",
                event_data={"new_level": new_level},
            )

            logger.info("Unlocked %d level achievements for user %s", len(unlocked), user_id)

        except Exception:
            logger.exception("Error handling LevelUp event")

    def _extract_new_level(self, event_data: dict) -> int:
        """Extract new level from event data."""
        return event_data.get("new_level", 1)
