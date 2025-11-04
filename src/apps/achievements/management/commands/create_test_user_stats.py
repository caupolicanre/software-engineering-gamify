"""Management command to create user statistics for testing."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.achievements.models import UserStatistics


User = get_user_model()


class Command(BaseCommand):
    """Create user statistics for existing users."""

    help = "Create user statistics for existing users"

    def add_arguments(self, parser) -> None:
        """Add command arguments."""
        parser.add_argument(
            "--user-id",
            type=int,
            help="Create stats for specific user ID",
        )

    def handle(self, *args, **options) -> None:
        """Handle the command to create user statistics."""
        user_id = options.get("user_id")

        users = User.objects.filter(id=user_id) if user_id else User.objects.all()

        created_count = 0
        for user in users:
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
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created stats for user: {user.username}"))
            else:
                self.stdout.write(self.style.WARNING(f"- Stats already exist for user: {user.username}"))

        self.stdout.write(self.style.SUCCESS(f"\nCreated statistics for {created_count} users"))
