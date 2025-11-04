"""Management command to create sample achievements for testing."""

from django.core.management.base import BaseCommand

from apps.achievements.models import Achievement


class Command(BaseCommand):
    """Create sample achievements for testing."""

    help = "Create sample achievements for testing"

    def handle(self, *args, **options) -> None:
        """Create sample achievements."""
        achievements = [
            {
                "name": "First Steps",
                "description": "Complete your first task",
                "criteria": {"required_count": 1, "type": "total"},
                "criteria_type": Achievement.CriteriaType.TASK_COUNT,
                "reward_xp": 100,
                "reward_coins": 10,
                "rarity": Achievement.Rarity.COMMON,
            },
            {
                "name": "Task Master",
                "description": "Complete 10 tasks",
                "criteria": {"required_count": 10, "type": "total"},
                "criteria_type": Achievement.CriteriaType.TASK_COUNT,
                "reward_xp": 500,
                "reward_coins": 50,
                "rarity": Achievement.Rarity.RARE,
            },
            {
                "name": "Century Club",
                "description": "Complete 100 tasks",
                "criteria": {"required_count": 100, "type": "total"},
                "criteria_type": Achievement.CriteriaType.TASK_COUNT,
                "reward_xp": 2000,
                "reward_coins": 200,
                "rarity": Achievement.Rarity.EPIC,
            },
            {
                "name": "Week Warrior",
                "description": "Maintain a 7-day streak",
                "criteria": {"required_days": 7, "type": "consecutive_days"},
                "criteria_type": Achievement.CriteriaType.STREAK,
                "reward_xp": 300,
                "reward_coins": 30,
                "rarity": Achievement.Rarity.RARE,
            },
            {
                "name": "Month Master",
                "description": "Maintain a 30-day streak",
                "criteria": {"required_days": 30, "type": "consecutive_days"},
                "criteria_type": Achievement.CriteriaType.STREAK,
                "reward_xp": 1500,
                "reward_coins": 150,
                "rarity": Achievement.Rarity.EPIC,
            },
            {
                "name": "Year Legend",
                "description": "Maintain a 365-day streak",
                "criteria": {"required_days": 365, "type": "consecutive_days"},
                "criteria_type": Achievement.CriteriaType.STREAK,
                "reward_xp": 10000,
                "reward_coins": 1000,
                "rarity": Achievement.Rarity.LEGENDARY,
            },
            {
                "name": "Level 10",
                "description": "Reach level 10",
                "criteria": {"required_level": 10},
                "criteria_type": Achievement.CriteriaType.LEVEL,
                "reward_xp": 1000,
                "reward_coins": 100,
                "rarity": Achievement.Rarity.RARE,
            },
            {
                "name": "Level 50",
                "description": "Reach level 50",
                "criteria": {"required_level": 50},
                "criteria_type": Achievement.CriteriaType.LEVEL,
                "reward_xp": 5000,
                "reward_coins": 500,
                "rarity": Achievement.Rarity.EPIC,
            },
            {
                "name": "Level 100",
                "description": "Reach level 100",
                "criteria": {"required_level": 100},
                "criteria_type": Achievement.CriteriaType.LEVEL,
                "reward_xp": 20000,
                "reward_coins": 2000,
                "rarity": Achievement.Rarity.LEGENDARY,
            },
        ]

        created_count = 0
        for ach_data in achievements:
            achievement, created = Achievement.objects.get_or_create(
                name=ach_data["name"],
                defaults=ach_data,
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Created achievement: {achievement.name}"),
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"- Achievement already exists: {achievement.name}"),
                )

        self.stdout.write(
            self.style.SUCCESS(f"\nCreated {created_count} new achievements"),
        )
