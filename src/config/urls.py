"""Main URL configuration with dynamic app URL discovery."""

import importlib

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def get_app_api_urls() -> list:
    """
    Dynamically discover and include API URLs from all apps.

    Looks for 'api/urls.py' in each app directory and includes them.

    Returns:
        list: List of URL patterns for all discovered app APIs
    """
    app_url_patterns = []

    for app_config in apps.get_app_configs():
        # Only process apps in our 'apps' directory
        if not app_config.name.startswith("apps."):
            continue

        app_name = app_config.name.split(".")[-1]  # Get last part: 'achievements', 'users', etc.

        try:
            # Try to import the api.urls module from the app
            api_urls_module = importlib.import_module(f"{app_config.name}.api.urls")

            # Include the app's API URLs
            app_url_patterns.append(
                path(f"{app_name}/", include((api_urls_module, app_name), namespace=app_name)),
            )

            print(f"✓ Loaded API URLs for app: {app_name}")

        except (ImportError, ModuleNotFoundError):
            # App doesn't have api/urls.py - skip silently
            pass

    return app_url_patterns


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # API v1 - Dynamically discovered app URLs
    path("api/v1/", include(get_app_api_urls())),
    # Legacy user API (if needed)
    path("api/", include("config.api_router")),
]

# Print discovered URLs in DEBUG mode
if settings.DEBUG:
    print("\n" + "=" * 50)
    print("Discovered API URLs:")
    print("=" * 50)
    discovered_urls = get_app_api_urls()
    for pattern in discovered_urls:
        print(f"  - /api/v1/{pattern.pattern}")
    print("=" * 50 + "\n")
