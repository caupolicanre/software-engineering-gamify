"""Tests for AchievementEvaluator."""

from decimal import Decimal

import pytest

from apps.achievements.models import Achievement, UserStatistics


pytestmark = pytest.mark.django_db


class TestAchievementEvaluator:
    """Test AchievementEvaluator class."""

    def test_evaluate_criteria_task_count_met(
        self,
        achievement_evaluator,
        user,
        task_count_achievement,
        user_stats,
    ):
        """Test evaluating task count criteria when met."""
        # user_stats has 10 tasks completed, achievement requires 10
        result = achievement_evaluator.evaluate_criteria(
            user.id,
            task_count_achievement,
            user_stats,
        )

        assert result is True

    def test_evaluate_criteria_task_count_not_met(
        self,
        achievement_evaluator,
        user,
        user_stats,
    ):
        """Test evaluating task count criteria when not met."""
        # Create achievement requiring 50 tasks
        achievement = Achievement.objects.create(
            name="Task Master Pro",
            description="Complete 50 tasks",
            criteria={"required_count": 50},
            criteria_type=Achievement.CriteriaType.TASK_COUNT,
        )

        # user_stats has only 10 tasks
        result = achievement_evaluator.evaluate_criteria(
            user.id,
            achievement,
            user_stats,
        )

        assert result is False

    def test_evaluate_criteria_streak_met(
        self,
        achievement_evaluator,
        user,
        user_stats,
    ):
        """Test evaluating streak criteria when met."""
        # user_stats has current_streak=5
        achievement = Achievement.objects.create(
            name="5 Day Streak",
            description="Maintain a 5-day streak",
            criteria={"required_days": 5},
            criteria_type=Achievement.CriteriaType.STREAK,
        )

        result = achievement_evaluator.evaluate_criteria(
            user.id,
            achievement,
            user_stats,
        )

        assert result is True

    def test_evaluate_criteria_streak_not_met(
        self,
        achievement_evaluator,
        user,
        streak_achievement,
        user_stats,
    ):
        """Test evaluating streak criteria when not met."""
        # streak_achievement requires 7 days, user has 5
        result = achievement_evaluator.evaluate_criteria(
            user.id,
            streak_achievement,
            user_stats,
        )

        assert result is False

    def test_evaluate_criteria_level_met(
        self,
        achievement_evaluator,
        user,
        user_stats,
    ):
        """Test evaluating level criteria when met."""
        # user_stats has current_level=3
        achievement = Achievement.objects.create(
            name="Level 3",
            description="Reach level 3",
            criteria={"required_level": 3},
            criteria_type=Achievement.CriteriaType.LEVEL,
        )

        result = achievement_evaluator.evaluate_criteria(
            user.id,
            achievement,
            user_stats,
        )

        assert result is True

    def test_evaluate_criteria_level_not_met(
        self,
        achievement_evaluator,
        user,
        level_achievement,
        user_stats,
    ):
        """Test evaluating level criteria when not met."""
        # level_achievement requires level 5, user has level 3
        result = achievement_evaluator.evaluate_criteria(
            user.id,
            level_achievement,
            user_stats,
        )

        assert result is False

    def test_evaluate_criteria_unsupported_type(
        self,
        achievement_evaluator,
        user,
        user_stats,
    ):
        """Test evaluating unsupported criteria type returns False."""
        # Create achievement with unsupported criteria type
        achievement = Achievement.objects.create(
            name="Friend Achievement",
            description="Add 5 friends",
            criteria={"required_count": 5},
            criteria_type=Achievement.CriteriaType.FRIEND_COUNT,
        )

        result = achievement_evaluator.evaluate_criteria(
            user.id,
            achievement,
            user_stats,
        )

        # Currently not implemented, should return False
        assert result is False

    def test_calculate_progress_task_count_half(
        self,
        achievement_evaluator,
        user,
        user_stats,
    ):
        """Test calculating progress for task count (50%)."""
        # Create achievement requiring 20 tasks, user has 10
        achievement = Achievement.objects.create(
            name="20 Tasks",
            description="Complete 20 tasks",
            criteria={"required_count": 20},
            criteria_type=Achievement.CriteriaType.TASK_COUNT,
        )

        progress = achievement_evaluator.calculate_progress(
            user.id,
            achievement,
            user_stats,
        )

        assert progress == Decimal("50.00")

    def test_calculate_progress_task_count_complete(
        self,
        achievement_evaluator,
        user,
        task_count_achievement,
        user_stats,
    ):
        """Test calculating progress for completed task count (100%)."""
        progress = achievement_evaluator.calculate_progress(
            user.id,
            task_count_achievement,
            user_stats,
        )

        assert progress == Decimal("100.00")

    def test_calculate_progress_streak_partial(
        self,
        achievement_evaluator,
        user,
        user_stats,
    ):
        """Test calculating progress for streak (partial)."""
        # Create achievement requiring 10 day streak, user has 5
        achievement = Achievement.objects.create(
            name="10 Day Streak",
            description="Maintain a 10-day streak",
            criteria={"required_days": 10},
            criteria_type=Achievement.CriteriaType.STREAK,
        )

        progress = achievement_evaluator.calculate_progress(
            user.id,
            achievement,
            user_stats,
        )

        assert progress == Decimal("50.00")

    def test_calculate_progress_level_partial(
        self,
        achievement_evaluator,
        user,
        level_achievement,
        user_stats,
    ):
        """Test calculating progress for level (partial)."""
        # level_achievement requires level 5, user has level 3
        progress = achievement_evaluator.calculate_progress(
            user.id,
            level_achievement,
            user_stats,
        )

        assert progress == Decimal("60.00")  # 3/5 = 60%

    def test_calculate_progress_exceeds_100(
        self,
        achievement_evaluator,
        user,
        user_stats,
    ):
        """Test that progress doesn't exceed 100%."""
        # Create achievement requiring 5 tasks, user has 10
        achievement = Achievement.objects.create(
            name="Easy Task",
            description="Complete 5 tasks",
            criteria={"required_count": 5},
            criteria_type=Achievement.CriteriaType.TASK_COUNT,
        )

        progress = achievement_evaluator.calculate_progress(
            user.id,
            achievement,
            user_stats,
        )

        assert progress == Decimal("100.00")

    def test_calculate_progress_unsupported_type(
        self,
        achievement_evaluator,
        user,
        user_stats,
    ):
        """Test calculating progress for unsupported type returns 0."""
        achievement = Achievement.objects.create(
            name="Friend Achievement",
            description="Add 5 friends",
            criteria={"required_count": 5},
            criteria_type=Achievement.CriteriaType.FRIEND_COUNT,
        )

        progress = achievement_evaluator.calculate_progress(
            user.id,
            achievement,
            user_stats,
        )

        # Currently not implemented, should return 0
        assert progress == Decimal("0.00")

    def test_get_user_statistics(self, achievement_evaluator, user, user_stats):
        """Test getting user statistics as dictionary."""
        stats_dict = achievement_evaluator.get_user_statistics(user.id)

        assert stats_dict["total_tasks_completed"] == 10
        assert stats_dict["current_streak"] == 5
        assert stats_dict["longest_streak"] == 7
        assert stats_dict["total_xp"] == 500
        assert stats_dict["current_level"] == 3
        assert stats_dict["friend_count"] == 2
        assert stats_dict["challenges_won"] == 1

    def test_get_user_statistics_not_found(self, achievement_evaluator, user):
        """Test getting statistics for user without statistics record."""
        # Delete stats if exists
        UserStatistics.objects.filter(user=user).delete()

        stats_dict = achievement_evaluator.get_user_statistics(user.id)

        assert stats_dict == {}
