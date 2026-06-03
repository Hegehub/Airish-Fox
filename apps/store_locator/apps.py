"""Store locator app config."""

from django.apps import AppConfig


class StoreLocatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.store_locator"
    verbose_name = "Магазины"
