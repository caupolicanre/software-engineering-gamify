"""TaskSimulationService - Simulates task completions for testing/demo purposes."""

import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from apps.achievements.events.handlers import TaskCompletedEventHandler
from apps.achievements.models import UserAchievement, UserStatistics


User = get_user_model()
logger = logging.getLogger(__name__)


class TaskSimulationService:
    """
    Simulates task completions for testing and demonstration purposes.

    This service mimics the behavior of the management command but provides
    an API-friendly interface for frontend integration.
    """

    def __init__(self) -> None:
        """Initialize the TaskSimulationService."""
        self.task_handler = TaskCompletedEventHandler()

    @transaction.atomic
    def simulate_task_completions(
        self,
        user_id: int,
        count: int,
        *,
        update_streak: bool = True,
    ) -> dict:
        """
        Simulate multiple task completions for a user.

        Args:
            user_id: User ID to simulate tasks for
            count: Number of tasks to simulate
            update_streak: Whether to update streak counter

        Returns:
            Dictionary with simulation results including:
                - tasks_completed: Number of tasks simulated
                - total_tasks_completed: Updated total
                - current_streak: Current streak value
                - longest_streak: Longest streak achieved
                - current_level: Current user level
                - total_xp: Total XP accumulated
                - achievements_unlocked: Number of achievements unlocked
                - unlocked_achievements: List of newly unlocked achievements
                - message: Success message

        Raises:
            ValueError: If user doesn't exist

        """
        logger.info("Simulating %d task completions for user %s", count, user_id)

        # Validate user exists
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist as exc:
            msg = f"User with ID {user_id} not found"
            raise ValueError(msg) from exc

        # Get or create user statistics
        stats, created = UserStatistics.objects.get_or_create(
            user=user,
            defaults={
                "total_tasks_completed": 0,
                "current_streak": 0,
                "longest_streak": 0,
                "total_xp": 0,
                "current_level": 1,
                "friend_count": 0,
                "challenges_won": 0,
            },
        )

        if created:
            logger.info("Created new statistics for user %s", user_id)

        # Track newly unlocked achievements
        newly_unlocked = []

        # Simulate each task completion
        for i in range(count):
            # Update statistics
            stats.total_tasks_completed += 1

            # Update streak if requested
            if update_streak and i == 0:  # Only update streak once per simulation batch
                stats.current_streak += 1
                stats.longest_streak = max(stats.longest_streak, stats.current_streak)

            # Calculate XP (50 XP per task as default)
            xp_earned = 50
            stats.total_xp += xp_earned

            # Calculate level based on XP (simple formula: level = 1 + XP // 1000)
            new_level = 1 + (stats.total_xp // 1000)
            if new_level > stats.current_level:
                stats.current_level = new_level
                logger.info("User %s leveled up to %d", user_id, new_level)

            stats.save()

            # Trigger event handler to check for achievements
            event_data = {
                "user_id": user_id,
                "task_id": f"simulated_task_{i + 1}",
                "difficulty": "medium",
                "timestamp": timezone.now().isoformat(),
                "xp_earned": xp_earned,
            }

            # Check for unlocked achievements
            self.task_handler.handle_task_completed(event_data)

            logger.debug("Simulated task #%d completion for user %s", i + 1, user_id)

        # Get newly unlocked achievements
        newly_unlocked = self._get_recently_unlocked_achievements(user_id)

        # Build result
        result = {
            "tasks_completed": count,
            "total_tasks_completed": stats.total_tasks_completed,
            "current_streak": stats.current_streak,
            "longest_streak": stats.longest_streak,
            "current_level": stats.current_level,
            "total_xp": stats.total_xp,
            "achievements_unlocked": len(newly_unlocked),
            "unlocked_achievements": self._format_achievements(newly_unlocked),
            "message": f"Successfully simulated {count} task completions for {user.username}",
        }

        logger.info(
            "Simulation complete for user %s: %d tasks, %d achievements unlocked",
            user_id,
            count,
            len(newly_unlocked),
        )

        return result

    def _get_recently_unlocked_achievements(self, user_id: int) -> list[UserAchievement]:
        """
        Get achievements that were unlocked during the simulation.

        Args:
            user_id: User ID

        Returns:
            List of UserAchievement instances unlocked recently

        """
        # Get all completed achievements for the user
        # We filter by those completed recently (last 5 minutes) as a heuristic
        recent_time = timezone.now() - timezone.timedelta(minutes=5)

        return list(
            UserAchievement.objects.filter(
                user_id=user_id,
                is_completed=True,
                unlocked_at__gte=recent_time,
            ).select_related("achievement"),
        )

    def _format_achievements(self, user_achievements: list[UserAchievement]) -> list[dict]:
        """
        Format achievement data for API response.

        Args:
            user_achievements: List of UserAchievement instances

        Returns:
            List of achievement dictionaries

        """
        return [
            {
                "id": str(ua.achievement.id),
                "name": ua.achievement.name,
                "description": ua.achievement.description,
                "rarity": ua.achievement.rarity,
                "reward_xp": ua.achievement.reward_xp,
                "reward_coins": ua.achievement.reward_coins,
                "unlocked_at": ua.unlocked_at.isoformat() if ua.unlocked_at else None,
            }
            for ua in user_achievements
        ]

    def get_user_statistics(self, user_id: int) -> dict:
        """
        Get current statistics for a user.

        Args:
            user_id: User ID

        Returns:
            Dictionary with user statistics

        Raises:
            ValueError: If user doesn't exist

        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist as exc:
            msg = f"User with ID {user_id} not found"
            raise ValueError(msg) from exc

        try:
            stats = UserStatistics.objects.get(user=user)
        except UserStatistics.DoesNotExist:
            # Return default values if no statistics exist
            return {
                "total_tasks_completed": 0,
                "current_streak": 0,
                "longest_streak": 0,
                "total_xp": 0,
                "current_level": 1,
                "friend_count": 0,
                "challenges_won": 0,
            }

        return {
            "total_tasks_completed": stats.total_tasks_completed,
            "current_streak": stats.current_streak,
            "longest_streak": stats.longest_streak,
            "total_xp": stats.total_xp,
            "current_level": stats.current_level,
            "friend_count": stats.friend_count,
            "challenges_won": stats.challenges_won,
        }
