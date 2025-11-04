"""Serializers for Achievement API."""

from rest_framework import serializers

from apps.achievements.models import Achievement, UserAchievement


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement model."""

    rarity_display = serializers.CharField(source="get_rarity_display", read_only=True)
    criteria_type_display = serializers.CharField(source="get_criteria_type_display", read_only=True)

    class Meta:
        model = Achievement
        fields = [
            "id",
            "name",
            "description",
            "criteria",
            "criteria_type",
            "criteria_type_display",
            "reward_xp",
            "reward_coins",
            "icon",
            "rarity",
            "rarity_display",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_criteria(self, value: dict) -> dict:
        """Validate criteria JSON format."""
        if not isinstance(value, dict):
            criteria_error = "Criteria must be a valid JSON object"
            raise serializers.ValidationError(criteria_error)

        # Add specific validation based on criteria_type
        # For now, just ensure it's a dict
        return value

    def validate_reward_xp(self, value: int) -> int:
        """Validate reward XP is non-negative."""
        if value < 0:
            reward_xp_error = "Reward XP must be non-negative"
            raise serializers.ValidationError(reward_xp_error)
        return value

    def validate_reward_coins(self, value: int) -> int:
        """Validate reward coins is non-negative."""
        if value < 0:
            reward_coins_error = "Reward coins must be non-negative"
            raise serializers.ValidationError(reward_coins_error)
        return value


class UserAchievementSerializer(serializers.ModelSerializer):
    """Serializer for UserAchievement model."""

    achievement = AchievementSerializer(read_only=True)
    achievement_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = UserAchievement
        fields = [
            "id",
            "user",
            "achievement",
            "achievement_id",
            "unlocked_at",
            "progress",
            "is_completed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "unlocked_at", "created_at", "updated_at"]

    def validate_progress(self, value: float) -> float:
        """Validate progress is between 0 and 100."""
        if value < 0 or value > 100:
            progress_error = "Progress must be between 0 and 100"
            raise serializers.ValidationError(progress_error)
        return value

    def create(self, validated_data: dict) -> UserAchievement:
        """Create UserAchievement instance."""
        # User is set from request context in viewset
        return super().create(validated_data)


class AchievementProgressSerializer(serializers.Serializer):
    """Serializer for achievement progress information."""

    achievement_id = serializers.UUIDField()
    achievement_name = serializers.CharField()
    current_progress = serializers.DecimalField(max_digits=5, decimal_places=2)
    required_progress = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    is_unlocked = serializers.BooleanField()

    def calculate_percentage(self) -> float:
        """Calculate percentage from current/required progress."""
        current = self.validated_data.get("current_progress", 0)
        required = self.validated_data.get("required_progress", 1)

        if required == 0:
            return 100.0

        return min(100.0, (float(current) / float(required)) * 100)


class UserAchievementListSerializer(serializers.Serializer):
    """Serializer for listing user achievements with progress."""

    achievement = AchievementSerializer()
    progress = serializers.DecimalField(max_digits=5, decimal_places=2)
    is_unlocked = serializers.BooleanField()
    unlocked_at = serializers.DateTimeField(allow_null=True)


class AchievementUnlockRequestSerializer(serializers.Serializer):
    """Serializer for achievement unlock request."""

    achievement_id = serializers.UUIDField(required=True)
    user_id = serializers.IntegerField(required=False, allow_null=True, help_text="Optional user ID for testing/demo purposes")

    def validate_achievement_id(self, value: str) -> str:
        """Validate achievement exists."""
        if not Achievement.objects.filter(id=value, is_active=True).exists():
            achievement_id_error = "Achievement does not exist or is not active"
            raise serializers.ValidationError(achievement_id_error)
        return value


class SimulateTaskCompletionSerializer(serializers.Serializer):
    """Serializer for simulating task completions."""

    user_id = serializers.IntegerField(required=False, allow_null=True, help_text="Optional user ID for testing/demo purposes")
    count = serializers.IntegerField(min_value=1, max_value=100, default=1, help_text="Number of tasks to simulate (1-100)")
    update_streak = serializers.BooleanField(default=True, help_text="Whether to update the streak counter")

    def validate_count(self, value: int) -> int:
        """Validate count is within reasonable limits."""
        if value < 1:
            count_error = "Count must be at least 1"
            raise serializers.ValidationError(count_error)
        if value > 100:
            count_error = "Count cannot exceed 100 tasks at once"
            raise serializers.ValidationError(count_error)
        return value


class TaskSimulationResultSerializer(serializers.Serializer):
    """Serializer for task simulation results."""

    tasks_completed = serializers.IntegerField()
    total_tasks_completed = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    longest_streak = serializers.IntegerField()
    current_level = serializers.IntegerField()
    total_xp = serializers.IntegerField()
    achievements_unlocked = serializers.IntegerField()
    unlocked_achievements = serializers.ListField(child=serializers.DictField())
    message = serializers.CharField()
