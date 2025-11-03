from gamify.users.models import User


def test_user_get_absolute_url(user: User) -> None:
    """Test that user.get_absolute_url() returns the correct URL."""
    assert user.get_absolute_url() == f"/users/{user.username}/"
