"""
Achievement Model - Represents available achievements in the system.
"""

import uuid

from django.contrib.auth import get_user_model
from django.db import models

from apps.achievements.managers.achievement_manager import AchievementManager


User = get_user_model()


class Achievement(models.Model):
    """
    Represents an achievement that users can unlock.

    Attributes:
        id: UUID primary key
        name: Achievement name
        description: Detailed description
        criteria: JSON field with unlock criteria
        criteria_type: Type of criteria (task_count, streak, level, etc.)
        reward_xp: XP reward for unlocking
        reward_coins: Coins reward for unlocking
        icon: URL to achievement icon
        rarity: Achievement rarity (common, rare, epic, legendary)
        is_active: Whether achievement is currently active

    """

    class Rarity(models.TextChoices):
        COMMON = "common", "Common"
        RARE = "rare", "Rare"
        EPIC = "epic", "Epic"
        LEGENDARY = "legendary", "Legendary"

    class CriteriaType(models.TextChoices):
        TASK_COUNT = "task_count", "Task Count"
        STREAK = "streak", "Streak"
        LEVEL = "level", "Level"
        FRIEND_COUNT = "friend_count", "Friend Count"
        CHALLENGE = "challenge", "Challenge"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    criteria = models.JSONField(
        help_text="JSON with criteria configuration, e.g., {'required_count': 7, 'type': 'consecutive_days'}",
    )
    criteria_type = models.CharField(
        max_length=20,
        choices=CriteriaType.choices,
        default=CriteriaType.TASK_COUNT,
    )
    reward_xp = models.PositiveIntegerField(default=0)
    reward_coins = models.PositiveIntegerField(default=0)
    icon = models.URLField(blank=True, null=True)
    rarity = models.CharField(
        max_length=20,
        choices=Rarity.choices,
        default=Rarity.COMMON,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AchievementManager()

    class Meta:
        db_table = "achievements"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["criteria_type", "is_active"]),
            models.Index(fields=["rarity"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_rarity_display()})"

    def is_unlockable_by(self, user_id):
        """
        Check if this achievement can be unlocked by a user.
        This is a placeholder - actual logic is in AchievementEvaluator.
        """
        from apps.achievements.models import UserAchievement

        return not UserAchievement.objects.filter(
            user_id=user_id,
            achievement=self,
            is_completed=True,
        ).exists()

    def get_rarity_display_with_emoji(self):
        """Get rarity display with emoji."""
        emoji_map = {
            self.Rarity.COMMON: "⚪",
            self.Rarity.RARE: "🔵",
            self.Rarity.EPIC: "🟣",
            self.Rarity.LEGENDARY: "🟠",
        }
        return f"{emoji_map.get(self.rarity, '')} {self.get_rarity_display()}"
