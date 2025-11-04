"""Utility for sending notifications via Notification Service."""

import logging

from django.conf import settings


logger = logging.getLogger(__name__)


class NotificationSender:
    """Sends notifications to users via Notification Service."""

    def __init__(self) -> None:
        """Initialize the NotificationSender."""
        self.notification_service_url = settings.NOTIFICATION_SERVICE_URL

    def send_achievement_notification(self, user_id: int, achievement_name: str, description: str) -> None:
        """
        Send notification about achievement unlock.

        Args:
            user_id: User ID
            achievement_name: Achievement name
            description: Achievement description
        """
        payload = self._build_notification_payload(
            user_id=user_id,
            title=f"🎉 Achievement Unlocked: {achievement_name}!",
            body=description,
            notification_type="achievement_unlocked",
            extra_data={
                "achievement_name": achievement_name,
            },
        )

        self._send_notification(payload)

    def send_progress_notification(self, user_id: int, achievement_name: str, progress: float) -> None:
        """
        Send notification about progress update.

        Args:
            user_id: User ID
            achievement_name: Achievement name
            progress: Progress percentage
        """
        payload = self._build_notification_payload(
            user_id=user_id,
            title=f"Progress Update: {achievement_name}",
            body=f"You're {progress:.0f}% of the way there!",
            notification_type="achievement_progress",
            extra_data={
                "achievement_name": achievement_name,
                "progress": progress,
            },
        )

        self._send_notification(payload)

    def _build_notification_payload(
        self, user_id: int, title: str, body: str, notification_type: str, extra_data: dict | None = None
    ) -> dict:
        """
        Build notification payload.

        Args:
            user_id: User ID
            title: Notification title
            body: Notification body
            notification_type: Type of notification
            extra_data: Extra data to include

        Returns:
            Notification payload dictionary
        """
        return {
            "user_id": user_id,
            "title": title,
            "body": body,
            "type": notification_type,
            "priority": "high",
            "data": extra_data or {},
        }

    def _send_notification(self, payload: dict) -> None:
        """
        Send notification to Notification Service.

        Args:
            payload: Notification payload
        """
        try:
            # TODO: Implement actual HTTP call to Notification Service
            # For now, just log
            logger.info("Sending notification: %s", payload)

            # In production:
            # response = requests.post(
            #     f"{self.notification_service_url}/api/notifications/send",
            #     json=payload,
            #     timeout=5
            # )
            # response.raise_for_status()

        except Exception:
            logger.exception("Error sending notification: %s")
