"""Tests for Achievement models."""

from decimal import Decimal

import pytest
from django.db import IntegrityError

from apps.achievements.models import Achievement, UserAchievement, UserStatistics


pytestmark = pytest.mark.django_db


class TestAchievementModel:
    """Test Achievement model."""

    def test_create_achievement(self):
        """Test creating an achievement."""
        achievement = Achievement.objects.create(
            name="Test Achievement",
            description="Test description",
            criteria={"required_count": 10},
            criteria_type=Achievement.CriteriaType.TASK_COUNT,
            reward_xp=100,
            reward_coins=50,
            rarity=Achievement.Rarity.COMMON,
        )

        assert achievement.name == "Test Achievement"
        assert achievement.description == "Test description"
        assert achievement.criteria == {"required_count": 10}
        assert achievement.criteria_type == Achievement.CriteriaType.TASK_COUNT
        assert achievement.reward_xp == 100
        assert achievement.reward_coins == 50
        assert achievement.rarity == Achievement.Rarity.COMMON
        assert achievement.is_active is True

    def test_achievement_str_representation(self, task_count_achievement):
        """Test achievement string representation."""
        result = str(task_count_achievement)
        assert "Task Master" in result
        assert "Common" in result

    def test_achievement_unique_name(self, task_count_achievement):
        """Test that achievement names must be unique."""
        with pytest.raises(IntegrityError):
            Achievement.objects.create(
                name="Task Master",
                description="Duplicate name",
                criteria={"required_count": 5},
                criteria_type=Achievement.CriteriaType.TASK_COUNT,
            )

    def test_achievement_default_values(self):
        """Test achievement default values."""
        achievement = Achievement.objects.create(
            name="Default Test",
            description="Testing defaults",
            criteria={},
        )

        assert achievement.criteria_type == Achievement.CriteriaType.TASK_COUNT
        assert achievement.reward_xp == 0
        assert achievement.reward_coins == 0
        assert achievement.icon == ""
        assert achievement.rarity == Achievement.Rarity.COMMON
        assert achievement.is_active is True

    def test_get_rarity_display_with_emoji(self):
        """Test getting rarity display with emoji."""
        common = Achievement.objects.create(
            name="Common Achievement",
            description="Common",
            criteria={},
            rarity=Achievement.Rarity.COMMON,
        )
        result = common.get_rarity_display_with_emoji()
        assert "⚪" in result
        assert "Common" in result

        rare = Achievement.objects.create(
            name="Rare Achievement",
            description="Rare",
            criteria={},
            rarity=Achievement.Rarity.RARE,
        )
        result = rare.get_rarity_display_with_emoji()
        assert "🔵" in result
        assert "Rare" in result

    def test_is_unlockable_by_user_not_unlocked(self, task_count_achievement, user):
        """Test is_unlockable_by when user has not unlocked achievement."""
        result = task_count_achievement.is_unlockable_by(user.id)
        assert result is True

    def test_is_unlockable_by_user_already_unlocked(self, unlocked_user_achievement):
        """Test is_unlockable_by when user has already unlocked achievement."""
        result = unlocked_user_achievement.achievement.is_unlockable_by(
            unlocked_user_achievement.user.id,
        )
        assert result is False


class TestUserAchievementModel:
    """Test UserAchievement model."""

    def test_create_user_achievement(self, user, task_count_achievement):
        """Test creating a user achievement."""
        user_achievement = UserAchievement.objects.create(
            user=user,
            achievement=task_count_achievement,
            progress=50.00,
        )

        assert user_achievement.user == user
        assert user_achievement.achievement == task_count_achievement
        assert user_achievement.progress == Decimal("50.00")
        assert user_achievement.is_completed is False
        assert user_achievement.unlocked_at is None

    def test_user_achievement_str_representation(self, unlocked_user_achievement):
        """Test user achievement string representation."""
        result = str(unlocked_user_achievement)
        assert "testuser" in result
        assert "Task Master" in result
        assert "Unlocked" in result

    def test_user_achievement_unique_together(self, user, task_count_achievement):
        """Test that user-achievement combination must be unique."""
        UserAchievement.objects.create(
            user=user,
            achievement=task_count_achievement,
        )

        with pytest.raises(IntegrityError):
            UserAchievement.objects.create(
                user=user,
                achievement=task_count_achievement,
            )

    def test_update_progress(self, in_progress_user_achievement):
        """Test updating progress."""
        initial_progress = in_progress_user_achievement.progress

        in_progress_user_achievement.update_progress(75.50)

        in_progress_user_achievement.refresh_from_db()
        assert in_progress_user_achievement.progress == Decimal("75.50")
        assert in_progress_user_achievement.progress > initial_progress

    def test_update_progress_max_100(self, in_progress_user_achievement):
        """Test that progress cannot exceed 100."""
        in_progress_user_achievement.update_progress(150.00)

        in_progress_user_achievement.refresh_from_db()
        assert in_progress_user_achievement.progress == Decimal("100.00")

    def test_update_progress_min_0(self, in_progress_user_achievement):
        """Test that progress cannot be negative."""
        in_progress_user_achievement.update_progress(-10.00)

        in_progress_user_achievement.refresh_from_db()
        assert in_progress_user_achievement.progress == Decimal("0.00")

    def test_complete_achievement(self, in_progress_user_achievement):
        """Test completing an achievement."""
        assert in_progress_user_achievement.is_completed is False
        assert in_progress_user_achievement.unlocked_at is None

        in_progress_user_achievement.complete()

        in_progress_user_achievement.refresh_from_db()
        assert in_progress_user_achievement.is_completed is True
        assert in_progress_user_achievement.progress == Decimal("100.00")
        assert in_progress_user_achievement.unlocked_at is not None

    def test_complete_already_completed(self, unlocked_user_achievement):
        """Test that completing an already completed achievement doesn't change unlocked_at."""
        original_unlocked_at = unlocked_user_achievement.unlocked_at

        unlocked_user_achievement.complete()

        unlocked_user_achievement.refresh_from_db()
        # Should remain the same
        assert unlocked_user_achievement.is_completed is True
        assert unlocked_user_achievement.unlocked_at == original_unlocked_at


class TestUserStatisticsModel:
    """Test UserStatistics model."""

    def test_create_user_statistics(self, user):
        """Test creating user statistics."""
        stats = UserStatistics.objects.create(user=user)

        assert stats.user == user
        assert stats.total_tasks_completed == 0
        assert stats.current_streak == 0
        assert stats.longest_streak == 0
        assert stats.total_xp == 0
        assert stats.current_level == 1
        assert stats.friend_count == 0
        assert stats.challenges_won == 0

    def test_user_statistics_str_representation(self, user_stats):
        """Test user statistics string representation."""
        result = str(user_stats)
        assert "testuser" in result
        assert "Level 3" in result
        assert "10 tasks" in result

    def test_user_statistics_one_to_one(self, user, user_stats):
        """Test that user can only have one statistics record."""
        with pytest.raises(IntegrityError):
            UserStatistics.objects.create(user=user)

    def test_update_stats(self, user_stats):
        """Test updating a specific statistic."""
        user_stats.update_stats("total_tasks_completed", 20)

        user_stats.refresh_from_db()
        assert user_stats.total_tasks_completed == 20

    def test_update_invalid_stat(self, user_stats):
        """Test updating a non-existent statistic does nothing."""
        user_stats.update_stats("invalid_stat", 100)

        # Should not raise error, just ignore
        user_stats.refresh_from_db()

    def test_increment_stat(self, user_stats):
        """Test incrementing a statistic."""
        initial_value = user_stats.total_tasks_completed

        user_stats.increment_stat("total_tasks_completed", 5)

        user_stats.refresh_from_db()
        assert user_stats.total_tasks_completed == initial_value + 5

    def test_increment_stat_default_increment(self, user_stats):
        """Test incrementing a statistic with default increment (1)."""
        initial_value = user_stats.current_streak

        user_stats.increment_stat("current_streak")

        user_stats.refresh_from_db()
        assert user_stats.current_streak == initial_value + 1

    def test_refresh_from_sources_placeholder(self, user_stats):
        """Test refresh_from_sources placeholder method."""
        # This is a placeholder method, should not raise error
        user_stats.refresh_from_sources()

        # No assertions, just verify it doesn't crash


class TestAchievementChoices:
    """Test Achievement model choices."""

    def test_rarity_choices(self):
        """Test that all rarity choices are available."""
        assert Achievement.Rarity.COMMON == "common"
        assert Achievement.Rarity.RARE == "rare"
        assert Achievement.Rarity.EPIC == "epic"
        assert Achievement.Rarity.LEGENDARY == "legendary"

        # Check choices count
        assert len(Achievement.Rarity.choices) == 4

    def test_criteria_type_choices(self):
        """Test that all criteria type choices are available."""
        assert Achievement.CriteriaType.TASK_COUNT == "task_count"
        assert Achievement.CriteriaType.STREAK == "streak"
        assert Achievement.CriteriaType.LEVEL == "level"
        assert Achievement.CriteriaType.FRIEND_COUNT == "friend_count"
        assert Achievement.CriteriaType.CHALLENGE == "challenge"

        # Check choices count
        assert len(Achievement.CriteriaType.choices) == 5
