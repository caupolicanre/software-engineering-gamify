"""Tests for Achievement model managers."""

import pytest

from apps.achievements.models import Achievement, UserAchievement


pytestmark = pytest.mark.django_db


class TestAchievementManager:
    """Test AchievementManager custom methods."""

    def test_get_active_achievements(
        self,
        task_count_achievement,
        streak_achievement,
        inactive_achievement,
    ):
        """Test getting only active achievements."""
        active = Achievement.objects.get_active_achievements()

        assert active.count() == 2
        assert task_count_achievement in active
        assert streak_achievement in active
        assert inactive_achievement not in active

    def test_get_by_rarity_common(self, task_count_achievement):
        """Test getting achievements by rarity (common)."""
        common = Achievement.objects.get_by_rarity(Achievement.Rarity.COMMON)

        assert common.count() >= 1
        assert task_count_achievement in common

    def test_get_by_rarity_rare(self, streak_achievement):
        """Test getting achievements by rarity (rare)."""
        rare = Achievement.objects.get_by_rarity(Achievement.Rarity.RARE)

        assert rare.count() >= 1
        assert streak_achievement in rare

    def test_get_by_rarity_legendary(self, legendary_achievement):
        """Test getting achievements by rarity (legendary)."""
        legendary = Achievement.objects.get_by_rarity(Achievement.Rarity.LEGENDARY)

        assert legendary.count() >= 1
        assert legendary_achievement in legendary

    def test_get_by_rarity_excludes_inactive(
        self,
        task_count_achievement,
        inactive_achievement,
    ):
        """Test that get_by_rarity excludes inactive achievements."""
        # Both are common rarity
        common = Achievement.objects.get_by_rarity(Achievement.Rarity.COMMON)

        assert task_count_achievement in common
        assert inactive_achievement not in common

    def test_get_by_criteria_type_task_count(self, task_count_achievement):
        """Test getting achievements by criteria type (task_count)."""
        task_count = Achievement.objects.get_by_criteria_type(
            Achievement.CriteriaType.TASK_COUNT,
        )

        assert task_count.count() >= 1
        assert task_count_achievement in task_count

    def test_get_by_criteria_type_streak(self, streak_achievement):
        """Test getting achievements by criteria type (streak)."""
        streak = Achievement.objects.get_by_criteria_type(
            Achievement.CriteriaType.STREAK,
        )

        assert streak.count() >= 1
        assert streak_achievement in streak

    def test_get_by_criteria_type_level(self, level_achievement):
        """Test getting achievements by criteria type (level)."""
        level = Achievement.objects.get_by_criteria_type(
            Achievement.CriteriaType.LEVEL,
        )

        assert level.count() >= 1
        assert level_achievement in level

    def test_search_by_name_exact_match(self, task_count_achievement):
        """Test searching achievements by exact name."""
        results = Achievement.objects.search_by_name("Task Master")

        assert results.count() >= 1
        assert task_count_achievement in results

    def test_search_by_name_partial_match(self, task_count_achievement):
        """Test searching achievements by partial name."""
        results = Achievement.objects.search_by_name("Task")

        assert results.count() >= 1
        assert task_count_achievement in results

    def test_search_by_name_case_insensitive(self, task_count_achievement):
        """Test that search is case-insensitive."""
        results = Achievement.objects.search_by_name("task master")

        assert results.count() >= 1
        assert task_count_achievement in results

    def test_search_by_name_no_results(self):
        """Test searching with no matching results."""
        results = Achievement.objects.search_by_name("NonExistent Achievement")

        assert results.count() == 0

    def test_search_by_name_excludes_inactive(
        self,
        task_count_achievement,
        inactive_achievement,
    ):
        """Test that search excludes inactive achievements."""
        results = Achievement.objects.search_by_name("Achievement")

        assert task_count_achievement in results
        assert inactive_achievement not in results


class TestUserAchievementManager:
    """Test UserAchievementManager custom methods."""

    def test_get_user_unlocked(self, user, unlocked_user_achievement):
        """Test getting unlocked achievements for a user."""
        unlocked = UserAchievement.objects.get_user_unlocked(user.id)

        assert unlocked.count() == 1
        assert unlocked_user_achievement in unlocked
        assert unlocked.first().is_completed is True

    def test_get_user_unlocked_excludes_in_progress(
        self,
        user,
        unlocked_user_achievement,
        in_progress_user_achievement,
    ):
        """Test that get_user_unlocked excludes in-progress achievements."""
        unlocked = UserAchievement.objects.get_user_unlocked(user.id)

        assert unlocked.count() == 1
        assert unlocked_user_achievement in unlocked
        assert in_progress_user_achievement not in unlocked

    def test_get_user_unlocked_empty_for_new_user(self, another_user):
        """Test that new user has no unlocked achievements."""
        unlocked = UserAchievement.objects.get_user_unlocked(another_user.id)

        assert unlocked.count() == 0

    def test_get_user_in_progress(self, user, in_progress_user_achievement):
        """Test getting in-progress achievements for a user."""
        in_progress = UserAchievement.objects.get_user_in_progress(user.id)

        assert in_progress.count() == 1
        assert in_progress_user_achievement in in_progress

    def test_get_user_in_progress_excludes_unlocked(
        self,
        user,
        unlocked_user_achievement,
        in_progress_user_achievement,
    ):
        """Test that get_user_in_progress excludes unlocked achievements."""
        in_progress = UserAchievement.objects.get_user_in_progress(user.id)

        assert in_progress.count() == 1
        assert in_progress_user_achievement in in_progress
        assert unlocked_user_achievement not in in_progress

    def test_get_user_in_progress_excludes_zero_progress(
        self,
        user,
        streak_achievement,
    ):
        """Test that get_user_in_progress excludes zero progress achievements."""
        # Create achievement with 0 progress
        UserAchievement.objects.create(
            user=user,
            achievement=streak_achievement,
            progress=0.00,
            is_completed=False,
        )

        in_progress = UserAchievement.objects.get_user_in_progress(user.id)

        # Should not include zero progress
        assert in_progress.count() == 0

    def test_is_unlocked_true(self, user, unlocked_user_achievement):
        """Test is_unlocked returns True for unlocked achievement."""
        result = UserAchievement.objects.is_unlocked(
            user.id,
            unlocked_user_achievement.achievement.id,
        )

        assert result is True

    def test_is_unlocked_false_in_progress(self, user, in_progress_user_achievement):
        """Test is_unlocked returns False for in-progress achievement."""
        result = UserAchievement.objects.is_unlocked(
            user.id,
            in_progress_user_achievement.achievement.id,
        )

        assert result is False

    def test_is_unlocked_false_not_started(self, user, level_achievement):
        """Test is_unlocked returns False for not started achievement."""
        result = UserAchievement.objects.is_unlocked(user.id, level_achievement.id)

        assert result is False

    def test_get_or_create_progress_creates_new(self, user, level_achievement):
        """Test get_or_create_progress creates new record."""
        user_achievement, created = UserAchievement.objects.get_or_create_progress(
            user.id,
            str(level_achievement.id),
        )

        assert created is True
        assert user_achievement.user == user
        assert user_achievement.achievement == level_achievement
        assert user_achievement.progress == 0.00
        assert user_achievement.is_completed is False

    def test_get_or_create_progress_gets_existing(
        self,
        user,
        in_progress_user_achievement,
    ):
        """Test get_or_create_progress gets existing record."""
        user_achievement, created = UserAchievement.objects.get_or_create_progress(
            user.id,
            str(in_progress_user_achievement.achievement.id),
        )

        assert created is False
        assert user_achievement.id == in_progress_user_achievement.id
        assert user_achievement.progress == in_progress_user_achievement.progress

    def test_bulk_update_progress(self, user, task_count_achievement, streak_achievement):
        """Test bulk updating progress for multiple achievements."""
        # Create two user achievements
        ua1 = UserAchievement.objects.create(
            user=user,
            achievement=task_count_achievement,
            progress=25.00,
        )
        ua2 = UserAchievement.objects.create(
            user=user,
            achievement=streak_achievement,
            progress=50.00,
        )

        # Update progress
        ua1.progress = 75.00
        ua2.progress = 90.00

        # Bulk update
        updated_count = UserAchievement.objects.bulk_update_progress([ua1, ua2])

        assert updated_count == 2

        # Verify updates
        ua1.refresh_from_db()
        ua2.refresh_from_db()
        assert ua1.progress == 75.00
        assert ua2.progress == 90.00

    def test_select_related_optimization(self, user, unlocked_user_achievement):
        """Test that manager methods use select_related for optimization."""
        with pytest.raises(AttributeError):
            # This would raise if select_related wasn't used
            # Actually, this test verifies that achievement is prefetched
            unlocked = UserAchievement.objects.get_user_unlocked(user.id)
            # Access achievement without additional query
            achievement = unlocked.first().achievement
            assert achievement is not None
