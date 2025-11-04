"""Pytest fixtures for achievements tests."""

import pytest
from django.contrib.auth import get_user_model

from apps.achievements.models import Achievement, UserAchievement, UserStatistics


User = get_user_model()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def user_with_stats(db, user):
    """Create a test user with statistics."""
    UserStatistics.objects.create(
        user=user,
        total_tasks_completed=5,
        current_streak=3,
        longest_streak=7,
        total_xp=500,
        current_level=3,
        friend_count=2,
        challenges_won=1,
    )
    return user


@pytest.fixture
def achievement_task_count(db):
    """Create a task count achievement."""
    return Achievement.objects.create(
        name="First Steps",
        description="Complete your first task",
        criteria={"required_count": 1, "type": "total"},
        criteria_type=Achievement.CriteriaType.TASK_COUNT,
        reward_xp=100,
        reward_coins=10,
        rarity=Achievement.Rarity.COMMON,
        is_active=True,
    )


@pytest.fixture
def achievement_streak(db):
    """Create a streak achievement."""
    return Achievement.objects.create(
        name="Week Warrior",
        description="Maintain a 7-day streak",
        criteria={"required_days": 7, "type": "consecutive_days"},
        criteria_type=Achievement.CriteriaType.STREAK,
        reward_xp=300,
        reward_coins=30,
        rarity=Achievement.Rarity.RARE,
        is_active=True,
    )


@pytest.fixture
def achievement_level(db):
    """Create a level achievement."""
    return Achievement.objects.create(
        name="Level 10",
        description="Reach level 10",
        criteria={"required_level": 10},
        criteria_type=Achievement.CriteriaType.LEVEL,
        reward_xp=1000,
        reward_coins=100,
        rarity=Achievement.Rarity.RARE,
        is_active=True,
    )


@pytest.fixture
def user_achievement_unlocked(db, user, achievement_task_count):
    """Create an unlocked user achievement."""
    return UserAchievement.objects.create(
        user=user,
        achievement=achievement_task_count,
        progress=100.00,
        is_completed=True,
    )


@pytest.fixture
def user_achievement_in_progress(db, user, achievement_streak):
    """Create a user achievement in progress."""
    return UserAchievement.objects.create(
        user=user,
        achievement=achievement_streak,
        progress=42.86,  # 3/7 days
        is_completed=False,
    )


@pytest.fixture
def api_client():
    """Create an API client."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Create an authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client
