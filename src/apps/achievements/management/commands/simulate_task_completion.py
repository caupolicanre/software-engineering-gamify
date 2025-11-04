"""Management command to simulate task completion events for testing."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.achievements.events.handlers import TaskCompletedEventHandler
from apps.achievements.models import UserStatistics


User = get_user_model()


class Command(BaseCommand):
    """Simulate task completion events for testing achievements."""

    help = "Simulate task completion events for testing achievements"

    def add_arguments(self, parser) -> None:
        """Add command arguments."""
        parser.add_argument(
            "--user-id",
            type=int,
            required=True,
            help="User ID to simulate tasks for",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=1,
            help="Number of tasks to simulate",
        )

    def handle(self, *args, **options) -> None:
        """Handle the command to simulate task completions."""
        user_id = options["user_id"]
        count = options["count"]

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"User with ID {user_id} not found"),
            )
            return

        # Get or create user statistics
        stats, _created = UserStatistics.objects.get_or_create(
            user=user,
            defaults={
                "total_tasks_completed": 0,
                "current_streak": 1,
                "current_level": 1,
            },
        )

        handler = TaskCompletedEventHandler()

        for i in range(count):
            # Update statistics
            stats.total_tasks_completed += 1
            stats.save()

            # Simulate event
            event_data = {
                "user_id": user_id,
                "task_id": f"task_{i + 1}",
                "difficulty": "medium",
                "timestamp": "2025-01-15T10:00:00Z",
                "xp_earned": 50,
            }

            handler.handle_task_completed(event_data)

            self.stdout.write(
                self.style.SUCCESS(f"✓ Simulated task #{i + 1} completion"),
            )

        self.stdout.write(
            self.style.SUCCESS(f"\nSimulated {count} task completions for {user.username}"),
        )
        self.stdout.write(
            f"Total tasks completed: {stats.total_tasks_completed}",
        )
