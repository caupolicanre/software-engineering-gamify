"""Achievement models package."""

import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .managers import AchievementManager, UserAchievementManager


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
        """Rarity levels for achievements."""

        COMMON = "common", "Common"
        RARE = "rare", "Rare"
        EPIC = "epic", "Epic"
        LEGENDARY = "legendary", "Legendary"

    class CriteriaType(models.TextChoices):
        """Types of criteria for unlocking achievements."""

        TASK_COUNT = "task_count", "Task Count"
        STREAK = "streak", "Streak"
        LEVEL = "level", "Level"
        FRIEND_COUNT = "friend_count", "Friend Count"
        CHALLENGE = "challenge", "Challenge"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    criteria = models.JSONField(help_text="JSON with criteria configuration, e.g., {'required_count': 7, 'type': 'consecutive_days'}")
    criteria_type = models.CharField(max_length=20, choices=CriteriaType.choices, default=CriteriaType.TASK_COUNT)
    reward_xp = models.PositiveIntegerField(default=0)
    reward_coins = models.PositiveIntegerField(default=0)
    icon = models.URLField(blank=True, default="")
    rarity = models.CharField(max_length=20, choices=Rarity.choices, default=Rarity.COMMON)
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

    def __str__(self) -> str:
        """
        Represent the achievement as a string.

        Returns:
            str: Achievement name and rarity.
        """
        return f"{self.name} ({self.get_rarity_display()})"

    def is_unlockable_by(self, user_id: int) -> bool:
        """
        Check if this achievement can be unlocked by a user.

        This is a placeholder - actual logic is in AchievementEvaluator.
        """
        return not UserAchievement.objects.filter(
            user_id=user_id,
            achievement=self,
            is_completed=True,
        ).exists()

    def get_rarity_display_with_emoji(self) -> str:
        """Get rarity display with emoji."""
        emoji_map = {
            self.Rarity.COMMON: "⚪",
            self.Rarity.RARE: "🔵",
            self.Rarity.EPIC: "🟣",
            self.Rarity.LEGENDARY: "🟠",
        }
        return f"{emoji_map.get(self.rarity, '')} {self.get_rarity_display()}"


class UserAchievement(models.Model):
    """
    Tracks the relationship between users and achievements.

    Attributes:
        id: UUID primary key
        user: Foreign key to User
        achievement: Foreign key to Achievement
        unlocked_at: Timestamp when unlocked (null if in progress)
        progress: Progress percentage (0.0 to 100.0)
        is_completed: Whether achievement is unlocked
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="user_achievements")
    unlocked_at = models.DateTimeField(null=True, blank=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Progress percentage (0.00 to 100.00)")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserAchievementManager()

    class Meta:
        db_table = "user_achievements"
        unique_together = [["user", "achievement"]]
        ordering = ["-unlocked_at", "-created_at"]
        indexes = [
            models.Index(fields=["user", "is_completed"]),
            models.Index(fields=["achievement", "is_completed"]),
        ]

    def __str__(self) -> str:
        """
        Represent the user achievement as a string.

        Returns:
            str: User and achievement status.
        """
        status = "Unlocked" if self.is_completed else f"{self.progress}% Complete"
        return f"{self.user} - {self.achievement.name} ({status})"

    def update_progress(self, new_progress: float) -> None:
        """
        Update progress percentage.

        Args:
            new_progress: New progress value (0-100)
        """
        self.progress = min(Decimal("100.00"), max(Decimal("0.00"), Decimal(str(new_progress))))
        self.save(update_fields=["progress", "updated_at"])

    def complete(self) -> None:
        """Mark achievement as completed."""
        if not self.is_completed:
            self.is_completed = True
            self.progress = 100.00
            self.unlocked_at = timezone.now()
            self.save(update_fields=["is_completed", "progress", "unlocked_at", "updated_at"])
