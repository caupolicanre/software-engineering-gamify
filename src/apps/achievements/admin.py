"""Django admin configuration for Achievement models."""

from django.contrib import admin

from apps.achievements.models import Achievement, UserAchievement, UserStatistics


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """Admin for Achievement model."""

    list_display = [
        "name",
        "rarity",
        "criteria_type",
        "reward_xp",
        "reward_coins",
        "is_active",
        "created_at",
    ]
    list_filter = ["rarity", "criteria_type", "is_active"]
    search_fields = ["name", "description"]
    readonly_fields = ["id", "created_at", "updated_at"]
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("id", "name", "description", "icon", "rarity", "is_active"),
            },
        ),
        (
            "Criteria",
            {
                "fields": ("criteria_type", "criteria"),
            },
        ),
        (
            "Rewards",
            {
                "fields": ("reward_xp", "reward_coins"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    """Admin for UserAchievement model."""

    list_display = [
        "user",
        "achievement",
        "progress",
        "is_completed",
        "unlocked_at",
        "created_at",
    ]
    list_filter = ["is_completed", "created_at"]
    search_fields = ["user__username", "achievement__name"]
    readonly_fields = ["id", "created_at", "updated_at"]
    raw_id_fields = ["user", "achievement"]


@admin.register(UserStatistics)
class UserStatisticsAdmin(admin.ModelAdmin):
    """Admin for UserStatistics model."""

    list_display = [
        "user",
        "total_tasks_completed",
        "current_streak",
        "current_level",
        "total_xp",
        "last_updated",
    ]
    search_fields = ["user__username"]
    readonly_fields = ["user", "last_updated"]
    fieldsets = (
        (
            "User",
            {
                "fields": ("user",),
            },
        ),
        (
            "Task Statistics",
            {
                "fields": ("total_tasks_completed",),
            },
        ),
        (
            "Streak Statistics",
            {
                "fields": ("current_streak", "longest_streak"),
            },
        ),
        (
            "Level and XP",
            {
                "fields": ("current_level", "total_xp"),
            },
        ),
        (
            "Social",
            {
                "fields": ("friend_count", "challenges_won"),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("last_updated",),
            },
        ),
    )
