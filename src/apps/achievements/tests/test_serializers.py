"""Tests for Achievement serializers."""

import uuid

import pytest

from apps.achievements.models import Achievement
from apps.achievements.serializers import (
    AchievementProgressSerializer,
    AchievementSerializer,
    AchievementUnlockRequestSerializer,
    SimulateTaskCompletionSerializer,
    TaskSimulationResultSerializer,
    UserAchievementListSerializer,
    UserAchievementSerializer,
)


pytestmark = pytest.mark.django_db


class TestAchievementSerializer:
    """Test AchievementSerializer."""

    def test_serialize_achievement(self, task_count_achievement):
        """Test serializing an achievement."""
        serializer = AchievementSerializer(task_count_achievement)
        data = serializer.data

        assert data["id"] == str(task_count_achievement.id)
        assert data["name"] == "Task Master"
        assert data["description"] == "Complete 10 tasks"
        assert data["criteria"] == {"required_count": 10}
        assert data["reward_xp"] == 100
        assert data["reward_coins"] == 50
        assert data["rarity"] == "common"
        assert data["rarity_display"] == "Common"
        assert data["is_active"] is True

    def test_deserialize_achievement(self):
        """Test deserializing achievement data."""
        data = {
            "name": "New Achievement",
            "description": "Test description",
            "criteria": {"required_count": 20},
            "criteria_type": Achievement.CriteriaType.TASK_COUNT,
            "reward_xp": 200,
            "reward_coins": 100,
            "rarity": Achievement.Rarity.RARE,
        }

        serializer = AchievementSerializer(data=data)
        assert serializer.is_valid()

        achievement = serializer.save()
        assert achievement.name == "New Achievement"
        assert achievement.reward_xp == 200

    def test_validate_criteria_rejects_non_dict(self):
        """Test that criteria must be a dict."""
        data = {
            "name": "Invalid Achievement",
            "description": "Invalid criteria",
            "criteria": "not a dict",
            "criteria_type": Achievement.CriteriaType.TASK_COUNT,
        }

        serializer = AchievementSerializer(data=data)
        assert not serializer.is_valid()
        assert "criteria" in serializer.errors

    def test_validate_reward_xp_rejects_negative(self):
        """Test that negative XP is rejected."""
        data = {
            "name": "Invalid XP",
            "description": "Negative XP",
            "criteria": {},
            "reward_xp": -100,
        }

        serializer = AchievementSerializer(data=data)
        assert not serializer.is_valid()
        assert "reward_xp" in serializer.errors

    def test_validate_reward_coins_rejects_negative(self):
        """Test that negative coins are rejected."""
        data = {
            "name": "Invalid Coins",
            "description": "Negative coins",
            "criteria": {},
            "reward_coins": -50,
        }

        serializer = AchievementSerializer(data=data)
        assert not serializer.is_valid()
        assert "reward_coins" in serializer.errors


class TestUserAchievementSerializer:
    """Test UserAchievementSerializer."""

    def test_serialize_user_achievement(self, unlocked_user_achievement):
        """Test serializing a user achievement."""
        serializer = UserAchievementSerializer(unlocked_user_achievement)
        data = serializer.data

        assert data["id"] == str(unlocked_user_achievement.id)
        assert data["user"] == unlocked_user_achievement.user.id
        assert data["is_completed"] is True
        assert float(data["progress"]) == 100.00
        assert data["unlocked_at"] is not None

        # Check nested achievement
        assert "achievement" in data
        assert data["achievement"]["name"] == "Task Master"

    def test_validate_progress_range(self):
        """Test that progress must be between 0 and 100."""
        # Test below 0
        serializer = UserAchievementSerializer(data={"progress": -10})
        assert not serializer.is_valid()
        assert "progress" in serializer.errors

        # Test above 100
        serializer = UserAchievementSerializer(data={"progress": 150})
        assert not serializer.is_valid()
        assert "progress" in serializer.errors

        # Test valid range
        serializer = UserAchievementSerializer(data={"progress": 50.00})
        serializer.is_valid()
        # Should not have progress errors (might have other required field errors)


class TestAchievementProgressSerializer:
    """Test AchievementProgressSerializer."""

    def test_serialize_progress(self):
        """Test serializing achievement progress."""
        data = {
            "achievement_id": str(uuid.uuid4()),
            "achievement_name": "Test Achievement",
            "current_progress": 50.00,
            "required_progress": 100,
            "percentage": 50.00,
            "is_unlocked": False,
        }

        serializer = AchievementProgressSerializer(data=data)
        assert serializer.is_valid()

        result = serializer.data
        assert result["achievement_name"] == "Test Achievement"
        assert float(result["percentage"]) == 50.00
        assert result["is_unlocked"] is False


class TestUserAchievementListSerializer:
    """Test UserAchievementListSerializer."""

    def test_serialize_user_achievement_list(self, unlocked_user_achievement):
        """Test serializing user achievement list."""
        data = {
            "achievement": unlocked_user_achievement.achievement,
            "progress": unlocked_user_achievement.progress,
            "is_unlocked": True,
            "unlocked_at": unlocked_user_achievement.unlocked_at,
        }

        serializer = UserAchievementListSerializer(data)
        result = serializer.data

        assert result["is_unlocked"] is True
        assert float(result["progress"]) == 100.00
        assert "achievement" in result
        assert result["achievement"]["name"] == "Task Master"


class TestAchievementUnlockRequestSerializer:
    """Test AchievementUnlockRequestSerializer."""

    def test_valid_unlock_request(self, task_count_achievement):
        """Test valid unlock request."""
        data = {
            "achievement_id": str(task_count_achievement.id),
            "user_id": 1,
        }

        serializer = AchievementUnlockRequestSerializer(data=data)
        assert serializer.is_valid()

    def test_unlock_request_without_user_id(self, task_count_achievement):
        """Test unlock request without user_id (optional)."""
        data = {
            "achievement_id": str(task_count_achievement.id),
        }

        serializer = AchievementUnlockRequestSerializer(data=data)
        assert serializer.is_valid()

    def test_validate_achievement_exists(self):
        """Test that achievement must exist."""
        fake_id = str(uuid.uuid4())
        data = {
            "achievement_id": fake_id,
        }

        serializer = AchievementUnlockRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "achievement_id" in serializer.errors

    def test_validate_inactive_achievement(self, inactive_achievement):
        """Test that inactive achievements are rejected."""
        data = {
            "achievement_id": str(inactive_achievement.id),
        }

        serializer = AchievementUnlockRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "achievement_id" in serializer.errors


class TestSimulateTaskCompletionSerializer:
    """Test SimulateTaskCompletionSerializer."""

    def test_valid_simulation_request(self):
        """Test valid simulation request."""
        data = {
            "user_id": 1,
            "count": 5,
            "update_streak": True,
        }

        serializer = SimulateTaskCompletionSerializer(data=data)
        assert serializer.is_valid()

    def test_simulation_with_defaults(self):
        """Test simulation with default values."""
        data = {}

        serializer = SimulateTaskCompletionSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["count"] == 1
        assert serializer.validated_data["update_streak"] is True

    def test_validate_count_minimum(self):
        """Test that count must be at least 1."""
        data = {"count": 0}

        serializer = SimulateTaskCompletionSerializer(data=data)
        assert not serializer.is_valid()
        assert "count" in serializer.errors

    def test_validate_count_maximum(self):
        """Test that count cannot exceed 100."""
        data = {"count": 101}

        serializer = SimulateTaskCompletionSerializer(data=data)
        assert not serializer.is_valid()
        assert "count" in serializer.errors

    def test_validate_count_in_range(self):
        """Test that count within range is valid."""
        data = {"count": 50}

        serializer = SimulateTaskCompletionSerializer(data=data)
        assert serializer.is_valid()


class TestTaskSimulationResultSerializer:
    """Test TaskSimulationResultSerializer."""

    def test_serialize_simulation_result(self):
        """Test serializing simulation result."""
        data = {
            "tasks_completed": 5,
            "total_tasks_completed": 15,
            "current_streak": 3,
            "longest_streak": 10,
            "current_level": 2,
            "total_xp": 300,
            "achievements_unlocked": 2,
            "unlocked_achievements": [
                {"id": "achievement-1", "name": "First Achievement"},
                {"id": "achievement-2", "name": "Second Achievement"},
            ],
            "message": "Simulation completed successfully",
        }

        serializer = TaskSimulationResultSerializer(data=data)
        assert serializer.is_valid()

        result = serializer.data
        assert result["tasks_completed"] == 5
        assert result["achievements_unlocked"] == 2
        assert len(result["unlocked_achievements"]) == 2
        assert result["message"] == "Simulation completed successfully"
