from django.conf import settings
from django.core.cache import cache

from .models import SiteSettings

SITE_SETTINGS_CACHE_KEY = 'airish_fox.site_settings'


def get_site_settings() -> SiteSettings:
    cached = cache.get(SITE_SETTINGS_CACHE_KEY)
    if cached is not None:
        return cached
    settings_obj = SiteSettings.objects.order_by('-updated_at').first()
    if settings_obj is None:
        settings_obj = SiteSettings(site_name='airish-fox')
    cache.set(SITE_SETTINGS_CACHE_KEY, settings_obj, timeout=getattr(settings, 'SITE_SETTINGS_CACHE_TIMEOUT', 300))
    return settings_obj


def clear_site_settings_cache() -> None:
    cache.delete(SITE_SETTINGS_CACHE_KEY)
