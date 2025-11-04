"""Tests for achievement validators."""

import pytest


pytestmark = pytest.mark.django_db


class TestAchievementValidator:
    """Test AchievementValidator class."""

    def test_validate_achievement_exists_true(
        self,
        achievement_validator,
        task_count_achievement,
    ):
        """Test that validate_achievement_exists returns True for existing achievement."""
        result = achievement_validator.validate_achievement_exists(
            str(task_count_achievement.id),
        )

        assert result is True

    def test_validate_achievement_exists_false(self, achievement_validator):
        """Test that validate_achievement_exists returns False for non-existent achievement."""
        import uuid

        fake_id = str(uuid.uuid4())
        result = achievement_validator.validate_achievement_exists(fake_id)

        assert result is False

    def test_validate_not_already_unlocked_true(
        self,
        achievement_validator,
        user,
        task_count_achievement,
    ):
        """Test that validate_not_already_unlocked returns True when not unlocked."""
        result = achievement_validator.validate_not_already_unlocked(
            user.id,
            str(task_count_achievement.id),
        )

        assert result is True

    def test_validate_not_already_unlocked_false(
        self,
        achievement_validator,
        user,
        unlocked_user_achievement,
    ):
        """Test that validate_not_already_unlocked returns False when already unlocked."""
        result = achievement_validator.validate_not_already_unlocked(
            user.id,
            str(unlocked_user_achievement.achievement.id),
        )

        assert result is False

    def test_validate_not_already_unlocked_in_progress(
        self,
        achievement_validator,
        user,
        in_progress_user_achievement,
    ):
        """Test that in-progress achievements are considered not unlocked."""
        result = achievement_validator.validate_not_already_unlocked(
            user.id,
            str(in_progress_user_achievement.achievement.id),
        )

        assert result is True

    def test_validate_criteria_format_valid_dict(self, achievement_validator):
        """Test that validate_criteria_format accepts valid dict."""
        criteria = {"required_count": 10, "type": "task_count"}
        result = achievement_validator.validate_criteria_format(criteria)

        assert result is True

    def test_validate_criteria_format_invalid_type(self, achievement_validator):
        """Test that validate_criteria_format rejects non-dict."""
        invalid_criteria = "not a dict"
        result = achievement_validator.validate_criteria_format(invalid_criteria)

        assert result is False

    def test_validate_criteria_format_empty_dict(self, achievement_validator):
        """Test that validate_criteria_format accepts empty dict."""
        result = achievement_validator.validate_criteria_format({})

        assert result is True

    def test_validate_user_eligible_true(
        self,
        achievement_validator,
        user,
        task_count_achievement,
    ):
        """Test that validate_user_eligible returns True for eligible user."""
        result = achievement_validator.validate_user_eligible(
            user.id,
            str(task_count_achievement.id),
        )

        assert result is True

    def test_validate_user_eligible_false_already_unlocked(
        self,
        achievement_validator,
        user,
        unlocked_user_achievement,
    ):
        """Test that validate_user_eligible returns False when already unlocked."""
        result = achievement_validator.validate_user_eligible(
            user.id,
            str(unlocked_user_achievement.achievement.id),
        )

        assert result is False

    def test_validate_user_eligible_false_inactive_achievement(
        self,
        achievement_validator,
        user,
        inactive_achievement,
    ):
        """Test that validate_user_eligible returns False for inactive achievement."""
        result = achievement_validator.validate_user_eligible(
            user.id,
            str(inactive_achievement.id),
        )

        assert result is False

    def test_validate_user_eligible_false_nonexistent_achievement(
        self,
        achievement_validator,
        user,
    ):
        """Test that validate_user_eligible returns False for non-existent achievement."""
        import uuid

        fake_id = str(uuid.uuid4())
        result = achievement_validator.validate_user_eligible(user.id, fake_id)

        assert result is False

    def test_validate_reward_values_valid(self, achievement_validator):
        """Test that validate_reward_values accepts valid positive values."""
        result = achievement_validator.validate_reward_values(100, 50)

        assert result is True

    def test_validate_reward_values_zero(self, achievement_validator):
        """Test that validate_reward_values accepts zero values."""
        result = achievement_validator.validate_reward_values(0, 0)

        assert result is True

    def test_validate_reward_values_negative_xp(self, achievement_validator):
        """Test that validate_reward_values rejects negative XP."""
        result = achievement_validator.validate_reward_values(-100, 50)

        assert result is False

    def test_validate_reward_values_negative_coins(self, achievement_validator):
        """Test that validate_reward_values rejects negative coins."""
        result = achievement_validator.validate_reward_values(100, -50)

        assert result is False

    def test_validate_reward_values_both_negative(self, achievement_validator):
        """Test that validate_reward_values rejects both negative values."""
        result = achievement_validator.validate_reward_values(-100, -50)

        assert result is False
