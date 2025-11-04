from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """Configuration for the Users app."""
    name = "apps.users"
    verbose_name = _("Users")
