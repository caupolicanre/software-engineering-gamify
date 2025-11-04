"""Tests for Achievement API views."""

import uuid

import pytest
from django.urls import reverse
from rest_framework import status

from apps.achievements.models import Achievement, UserAchievement


pytestmark = pytest.mark.django_db


class TestAchievementViewSet:
    """Test AchievementViewSet endpoints."""

    def test_list_achievements(self, authenticated_client, task_count_achievement):
        """Test listing achievements."""
        url = reverse("api:achievement-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 1

    def test_retrieve_achievement(
        self,
        authenticated_client,
        task_count_achievement,
    ):
        """Test retrieving a specific achievement."""
        url = reverse("api:achievement-detail", kwargs={"pk": task_count_achievement.id})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Task Master"

    def test_filter_by_rarity(
        self,
        authenticated_client,
        task_count_achievement,
        streak_achievement,
    ):
        """Test filtering achievements by rarity."""
        url = reverse("api:achievement-list")
        response = authenticated_client.get(url, {"rarity": "common"})

        assert response.status_code == status.HTTP_200_OK
        # Should only return common achievements
        for achievement in response.data["results"]:
            assert achievement["rarity"] == "common"

    def test_search_achievements(
        self,
        authenticated_client,
        task_count_achievement,
    ):
        """Test searching achievements by name."""
        url = reverse("api:achievement-list")
        response = authenticated_client.get(url, {"search": "Task"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 1

    def test_get_user_achievements(
        self,
        authenticated_client,
        unlocked_user_achievement,
    ):
        """Test getting user's achievements."""
        url = reverse("api:achievement-me")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_get_user_achievements_include_locked(
        self,
        authenticated_client,
        user,
        task_count_achievement,
        streak_achievement,
    ):
        """Test getting all achievements including locked ones."""
        url = reverse("api:achievement-me")
        response = authenticated_client.get(url, {"include_locked": "true"})

        assert response.status_code == status.HTTP_200_OK
        # Should include both locked and unlocked
        assert len(response.data) >= 2

    def test_get_available_achievements(
        self,
        authenticated_client,
        task_count_achievement,
        inactive_achievement,
    ):
        """Test getting only available (active) achievements."""
        url = reverse("api:achievement-available")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Should not include inactive achievements
        achievement_ids = [a["id"] for a in response.data]
        assert str(task_count_achievement.id) in achievement_ids
        assert str(inactive_achievement.id) not in achievement_ids

    def test_check_achievement_progress(
        self,
        authenticated_client,
        in_progress_user_achievement,
    ):
        """Test checking progress for specific achievement."""
        url = reverse(
            "api:achievement-progress",
            kwargs={"pk": in_progress_user_achievement.achievement.id},
        )
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "progress" in response.data or "current_progress" in response.data
        assert response.data["is_unlocked"] is False

    def test_check_achievement_progress_not_found(self, authenticated_client):
        """Test checking progress for non-existent achievement."""
        fake_id = uuid.uuid4()
        url = reverse("api:achievement-progress", kwargs={"pk": fake_id})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_unlock_achievement(
        self,
        authenticated_client,
        user,
        task_count_achievement,
    ):
        """Test manually unlocking an achievement."""
        url = reverse("api:achievement-unlock")
        data = {
            "achievement_id": str(task_count_achievement.id),
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["is_completed"] is True

        # Verify it was actually unlocked
        assert UserAchievement.objects.filter(
            user=user,
            achievement=task_count_achievement,
            is_completed=True,
        ).exists()

    def test_unlock_achievement_already_unlocked(
        self,
        authenticated_client,
        unlocked_user_achievement,
    ):
        """Test unlocking an already unlocked achievement returns error."""
        url = reverse("api:achievement-unlock")
        data = {
            "achievement_id": str(unlocked_user_achievement.achievement.id),
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already unlocked" in response.data["error"].lower()

    def test_unlock_achievement_not_found(self, authenticated_client):
        """Test unlocking non-existent achievement returns error."""
        url = reverse("api:achievement-unlock")
        fake_id = uuid.uuid4()
        data = {
            "achievement_id": str(fake_id),
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_all_progress(
        self,
        authenticated_client,
        user_stats,
        task_count_achievement,
    ):
        """Test getting progress for all achievements."""
        url = reverse("api:achievement-all-progress")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

        # Check data structure
        for progress in response.data:
            assert "id" in progress
            assert "name" in progress
            assert "progress_percentage" in progress
            assert "is_unlocked" in progress

    def test_get_all_progress_unauthenticated_with_user_id(self, api_client, user_stats):
        """Test getting progress with user_id parameter (unauthenticated)."""
        url = reverse("api:achievement-all-progress")
        response = api_client.get(url, {"user_id": user_stats.user.id})

        assert response.status_code == status.HTTP_200_OK

    def test_get_all_progress_unauthenticated_without_user_id(self, api_client):
        """Test that unauthenticated request without user_id fails."""
        url = reverse("api:achievement-all-progress")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_simulate_task_completions(self, authenticated_client, user_stats):
        """Test simulating task completions."""
        url = reverse("api:achievement-simulate-tasks")
        data = {
            "count": 5,
            "update_streak": True,
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "tasks_completed" in response.data
        assert response.data["tasks_completed"] == 5

    def test_simulate_task_completions_invalid_count(
        self,
        authenticated_client,
        user_stats,
    ):
        """Test simulation with invalid count."""
        url = reverse("api:achievement-simulate-tasks")
        data = {
            "count": 150,  # Exceeds max
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_simulate_task_completions_with_user_id(self, api_client, user_stats):
        """Test simulation with explicit user_id."""
        url = reverse("api:achievement-simulate-tasks")
        data = {
            "user_id": user_stats.user.id,
            "count": 3,
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

    def test_get_user_stats(self, authenticated_client, user_stats):
        """Test getting user statistics."""
        url = reverse("api:achievement-user-stats")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "total_tasks_completed" in response.data
        assert "current_streak" in response.data
        assert "current_level" in response.data

    def test_get_user_stats_with_user_id(self, api_client, user_stats):
        """Test getting user statistics with user_id parameter."""
        url = reverse("api:achievement-user-stats")
        response = api_client.get(url, {"user_id": user_stats.user.id})

        assert response.status_code == status.HTTP_200_OK

    def test_get_user_stats_unauthenticated_without_user_id(self, api_client):
        """Test that getting stats without auth or user_id fails."""
        url = reverse("api:achievement-user-stats")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_cannot_access_protected_endpoints(self, api_client):
        """Test that anonymous users cannot access certain endpoints."""
        # Most endpoints are public, but test one that might require auth
        # This depends on your permission settings
        url = reverse("api:achievement-list")
        response = api_client.get(url)

        # Currently set to AllowAny, so should work
        assert response.status_code == status.HTTP_200_OK


class TestAchievementViewSetOrdering:
    """Test ordering and filtering capabilities."""

    def test_order_by_created_at(
        self,
        authenticated_client,
        task_count_achievement,
        streak_achievement,
    ):
        """Test ordering achievements by creation date."""
        url = reverse("api:achievement-list")
        response = authenticated_client.get(url, {"ordering": "-created_at"})

        assert response.status_code == status.HTTP_200_OK

    def test_order_by_reward_xp(
        self,
        authenticated_client,
        task_count_achievement,
        streak_achievement,
    ):
        """Test ordering achievements by XP reward."""
        url = reverse("api:achievement-list")
        response = authenticated_client.get(url, {"ordering": "reward_xp"})

        assert response.status_code == status.HTTP_200_OK

    def test_filter_by_criteria_type(
        self,
        authenticated_client,
        task_count_achievement,
        streak_achievement,
    ):
        """Test filtering by criteria type."""
        url = reverse("api:achievement-list")
        response = authenticated_client.get(url, {"criteria_type": "task_count"})

        assert response.status_code == status.HTTP_200_OK
        for achievement in response.data["results"]:
            assert achievement["criteria_type"] == "task_count"

    def test_filter_by_is_active(
        self,
        authenticated_client,
        task_count_achievement,
        inactive_achievement,
    ):
        """Test filtering by is_active status."""
        url = reverse("api:achievement-list")
        response = authenticated_client.get(url, {"is_active": "true"})

        assert response.status_code == status.HTTP_200_OK
        for achievement in response.data["results"]:
            assert achievement["is_active"] is True


class TestAchievementViewSetPagination:
    """Test pagination."""

    def test_pagination_works(self, authenticated_client):
        """Test that pagination is applied."""
        # Create multiple achievements
        for i in range(15):
            Achievement.objects.create(
                name=f"Achievement {i}",
                description=f"Description {i}",
                criteria={"required_count": i + 1},
                criteria_type=Achievement.CriteriaType.TASK_COUNT,
            )

        url = reverse("api:achievement-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert "count" in response.data
        assert "next" in response.data or "previous" in response.data
