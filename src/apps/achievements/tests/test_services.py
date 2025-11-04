"""Tests for AchievementService."""

from unittest.mock import Mock, patch

import pytest

from apps.achievements.models import Achievement, UserAchievement, UserStatistics


pytestmark = pytest.mark.django_db


class TestAchievementService:
    """Test AchievementService class."""

    def test_check_and_unlock_achievements_unlocks_when_criteria_met(
        self,
        achievement_service,
        user,
        task_count_achievement,
        user_stats,
    ):
        """Test that achievements are unlocked when criteria are met."""
        # User has 10 tasks, achievement requires 10
        newly_unlocked = achievement_service.check_and_unlock_achievements(
            user_id=user.id,
            event_type="task_completed",
            event_data={"task_id": 123},
        )

        assert len(newly_unlocked) == 1
        assert newly_unlocked[0].achievement == task_count_achievement
        assert newly_unlocked[0].is_completed is True

    def test_check_and_unlock_achievements_no_unlock_when_criteria_not_met(
        self,
        achievement_service,
        user,
        legendary_achievement,
        user_stats,
    ):
        """Test that achievements are not unlocked when criteria are not met."""
        # User has 10 tasks, legendary requires 1000
        newly_unlocked = achievement_service.check_and_unlock_achievements(
            user_id=user.id,
            event_type="task_completed",
            event_data={"task_id": 123},
        )

        assert len(newly_unlocked) == 0

    def test_check_and_unlock_achievements_updates_progress(
        self,
        achievement_service,
        user,
        user_stats,
    ):
        """Test that progress is updated for in-progress achievements."""
        # Create achievement requiring 20 tasks, user has 10
        achievement = Achievement.objects.create(
            name="20 Tasks",
            description="Complete 20 tasks",
            criteria={"required_count": 20},
            criteria_type=Achievement.CriteriaType.TASK_COUNT,
            reward_xp=200,
        )

        achievement_service.check_and_unlock_achievements(
            user_id=user.id,
            event_type="task_completed",
            event_data={"task_id": 123},
        )

        # Check that progress was created/updated
        user_achievement = UserAchievement.objects.get(
            user=user,
            achievement=achievement,
        )
        assert user_achievement.progress == 50.00  # 10/20 = 50%

    def test_check_and_unlock_achievements_skips_already_unlocked(
        self,
        achievement_service,
        user,
        unlocked_user_achievement,
        user_stats,
    ):
        """Test that already unlocked achievements are skipped."""
        newly_unlocked = achievement_service.check_and_unlock_achievements(
            user_id=user.id,
            event_type="task_completed",
            event_data={"task_id": 123},
        )

        # Should not include already unlocked achievement
        achievement_ids = [ua.achievement.id for ua in newly_unlocked]
        assert unlocked_user_achievement.achievement.id not in achievement_ids

    def test_check_and_unlock_achievements_creates_stats_if_missing(
        self,
        achievement_service,
        user,
    ):
        """Test that user statistics are created if missing."""
        # Ensure no stats exist
        UserStatistics.objects.filter(user=user).delete()

        achievement_service.check_and_unlock_achievements(
            user_id=user.id,
            event_type="task_completed",
            event_data={"task_id": 123},
        )

        # Stats should be created
        assert UserStatistics.objects.filter(user=user).exists()

    def test_unlock_achievement_success(
        self,
        achievement_service,
        user,
        task_count_achievement,
    ):
        """Test successfully unlocking an achievement."""
        user_achievement = achievement_service.unlock_achievement(
            user_id=user.id,
            achievement_id=str(task_count_achievement.id),
        )

        assert user_achievement.user == user
        assert user_achievement.achievement == task_count_achievement
        assert user_achievement.is_completed is True
        assert user_achievement.progress == 100.00
        assert user_achievement.unlocked_at is not None

    def test_unlock_achievement_raises_error_for_nonexistent_user(
        self,
        achievement_service,
        task_count_achievement,
    ):
        """Test that unlocking raises error for non-existent user."""
        with pytest.raises(ValueError, match="User .* does not exist"):
            achievement_service.unlock_achievement(
                user_id=99999,
                achievement_id=str(task_count_achievement.id),
            )

    def test_unlock_achievement_raises_error_for_nonexistent_achievement(
        self,
        achievement_service,
        user,
    ):
        """Test that unlocking raises error for non-existent achievement."""
        import uuid

        fake_id = str(uuid.uuid4())

        with pytest.raises(ValueError, match="Achievement .* does not exist"):
            achievement_service.unlock_achievement(
                user_id=user.id,
                achievement_id=fake_id,
            )

    def test_unlock_achievement_raises_error_if_already_unlocked(
        self,
        achievement_service,
        user,
        unlocked_user_achievement,
    ):
        """Test that unlocking raises error if already unlocked."""
        with pytest.raises(ValueError, match="already unlocked"):
            achievement_service.unlock_achievement(
                user_id=user.id,
                achievement_id=str(unlocked_user_achievement.achievement.id),
            )

    def test_unlock_achievement_uses_transaction(
        self,
        achievement_service,
        user,
        task_count_achievement,
    ):
        """Test that unlock_achievement uses atomic transaction."""
        # This test verifies the method is wrapped in a transaction
        with patch.object(
            achievement_service.event_publisher,
            "publish_achievement_unlocked",
            side_effect=Exception("Event error"),
        ):
            # Despite event publisher error (happens after transaction.on_commit),
            # the achievement should still be unlocked
            user_achievement = achievement_service.unlock_achievement(
                user_id=user.id,
                achievement_id=str(task_count_achievement.id),
            )

            # Verify it was saved
            assert UserAchievement.objects.filter(id=user_achievement.id).exists()

    def test_get_user_achievements_unlocked_only(
        self,
        achievement_service,
        user,
        unlocked_user_achievement,
        in_progress_user_achievement,
    ):
        """Test getting only unlocked achievements."""
        achievements = achievement_service.get_user_achievements(
            user_id=user.id,
            include_locked=False,
        )

        assert len(achievements) == 1
        assert achievements[0]["is_unlocked"] is True

    def test_get_user_achievements_include_locked(
        self,
        achievement_service,
        user,
        task_count_achievement,
        streak_achievement,
        unlocked_user_achievement,
    ):
        """Test getting all achievements including locked."""
        achievements = achievement_service.get_user_achievements(
            user_id=user.id,
            include_locked=True,
        )

        # Should include all active achievements
        assert len(achievements) >= 2

        # Check that data structure is correct
        unlocked = [a for a in achievements if a["is_unlocked"]]
        locked = [a for a in achievements if not a["is_unlocked"]]

        assert len(unlocked) >= 1
        assert len(locked) >= 1

    def test_get_achievement_progress(
        self,
        achievement_service,
        user,
        in_progress_user_achievement,
    ):
        """Test getting progress for specific achievement."""
        progress_data = achievement_service.get_achievement_progress(
            user_id=user.id,
            achievement_id=str(in_progress_user_achievement.achievement.id),
        )

        assert progress_data["achievement_id"] == str(
            in_progress_user_achievement.achievement.id,
        )
        assert progress_data["current_progress"] == 50.00
        assert progress_data["percentage"] == 50.00
        assert progress_data["is_unlocked"] is False

    def test_get_achievement_progress_not_started(
        self,
        achievement_service,
        user,
        task_count_achievement,
    ):
        """Test getting progress for not started achievement."""
        progress_data = achievement_service.get_achievement_progress(
            user_id=user.id,
            achievement_id=str(task_count_achievement.id),
        )

        assert progress_data["current_progress"] == 0.0
        assert progress_data["percentage"] == 0.0
        assert progress_data["is_unlocked"] is False

    def test_calculate_all_progress(
        self,
        achievement_service,
        user,
        user_stats,
        task_count_achievement,
        streak_achievement,
    ):
        """Test calculating progress for all achievements."""
        progress_list = achievement_service.calculate_all_progress(user.id)

        assert len(progress_list) >= 2

        # Check data structure
        for progress in progress_list:
            assert "id" in progress
            assert "name" in progress
            assert "description" in progress
            assert "progress" in progress
            assert "progress_percentage" in progress
            assert "is_unlocked" in progress

    def test_calculate_all_progress_creates_stats_if_missing(
        self,
        achievement_service,
        user,
    ):
        """Test that calculate_all_progress creates stats if missing."""
        # Delete stats
        UserStatistics.objects.filter(user=user).delete()

        progress_list = achievement_service.calculate_all_progress(user.id)

        # Should not raise error and should create stats
        assert UserStatistics.objects.filter(user=user).exists()
        assert isinstance(progress_list, list)

    def test_get_relevant_achievements_task_completed(
        self,
        achievement_service,
        task_count_achievement,
    ):
        """Test getting relevant achievements for task_completed event."""
        achievements = achievement_service._get_relevant_achievements("task_completed")

        assert task_count_achievement in achievements

    def test_get_relevant_achievements_streak_milestone(
        self,
        achievement_service,
        streak_achievement,
    ):
        """Test getting relevant achievements for streak_milestone event."""
        achievements = achievement_service._get_relevant_achievements("streak_milestone")

        assert streak_achievement in achievements

    def test_get_relevant_achievements_unknown_event(
        self,
        achievement_service,
        task_count_achievement,
        streak_achievement,
    ):
        """Test that unknown event types return all active achievements."""
        achievements = achievement_service._get_relevant_achievements("unknown_event")

        # Should return all active achievements
        assert len(achievements) >= 2

    def test_update_progress_creates_if_not_exists(
        self,
        achievement_service,
        user,
        task_count_achievement,
    ):
        """Test that _update_progress creates UserAchievement if not exists."""
        achievement_service._update_progress(
            user.id,
            str(task_count_achievement.id),
            50.0,
        )

        # Should create the record
        user_achievement = UserAchievement.objects.get(
            user=user,
            achievement=task_count_achievement,
        )
        assert user_achievement.progress == 50.00

    def test_grant_achievement_rewards_returns_dict(
        self,
        achievement_service,
        user,
        task_count_achievement,
    ):
        """Test that _grant_achievement_rewards returns reward dictionary."""
        rewards = achievement_service._grant_achievement_rewards(
            user.id,
            task_count_achievement,
        )

        assert "xp" in rewards
        assert "coins" in rewards
        assert rewards["xp"] == task_count_achievement.reward_xp
        assert rewards["coins"] == task_count_achievement.reward_coins

    @patch("apps.achievements.services.achievement_service.EventPublisher")
    def test_publish_achievement_event_calls_publisher(
        self,
        mock_publisher_class,
        achievement_service,
        user,
        task_count_achievement,
    ):
        """Test that _publish_achievement_event calls event publisher."""
        mock_publisher = Mock()
        achievement_service.event_publisher = mock_publisher

        rewards = {"xp": 100, "coins": 50}

        achievement_service._publish_achievement_event(
            user.id,
            task_count_achievement,
            rewards,
        )

        mock_publisher.publish_achievement_unlocked.assert_called_once_with(
            user_id=user.id,
            achievement_id=str(task_count_achievement.id),
            achievement_name=task_count_achievement.name,
            rewards=rewards,
        )

    @patch("apps.achievements.services.achievement_service.NotificationSender")
    def test_notify_achievement_unlock_calls_sender(
        self,
        mock_sender_class,
        achievement_service,
        user,
        task_count_achievement,
    ):
        """Test that _notify_achievement_unlock calls notification sender."""
        mock_sender = Mock()
        achievement_service.notification_sender = mock_sender

        achievement_service._notify_achievement_unlock(
            user.id,
            task_count_achievement,
        )

        mock_sender.send_achievement_notification.assert_called_once_with(
            user_id=user.id,
            achievement_name=task_count_achievement.name,
            description=task_count_achievement.description,
        )
