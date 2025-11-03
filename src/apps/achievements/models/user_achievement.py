"""
UserAchievement Model - Tracks user progress and unlocks for achievements.
"""

import uuid

from django.contrib.auth import get_user_model
from django.db import models

from apps.achievements.managers.user_achievement_manager import UserAchievementManager
from apps.achievements.models.achievement import Achievement


User = get_user_model()


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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_achievements",
    )
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name="user_achievements",
    )
    unlocked_at = models.DateTimeField(null=True, blank=True)
    progress = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Progress percentage (0.00 to 100.00)",
    )
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

    def __str__(self):
        status = "Unlocked" if self.is_completed else f"{self.progress}% Complete"
        return f"{self.user} - {self.achievement.name} ({status})"

    def update_progress(self, new_progress):
        """
        Update progress percentage.

        Args:
            new_progress: New progress value (0-100)

        """
        from decimal import Decimal

        self.progress = min(Decimal("100.00"), max(Decimal("0.00"), Decimal(str(new_progress))))
        self.save(update_fields=["progress", "updated_at"])

    def complete(self):
        """Mark achievement as completed."""
        from django.utils import timezone

        if not self.is_completed:
            self.is_completed = True
            self.progress = 100.00
            self.unlocked_at = timezone.now()
            self.save(update_fields=["is_completed", "progress", "unlocked_at", "updated_at"])
