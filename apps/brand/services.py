"""Brand feature selectors with lightweight cache."""
from django.core.cache import cache

from .models import BrandBadge, BrandFeatureToggle, HomepageStoryBlock

CACHE_SECONDS = 60

def is_feature_enabled(key: str, default: bool = True) -> bool:
    cache_key = f"brand:feature:{key}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    enabled = BrandFeatureToggle.objects.filter(key=key).values_list("is_enabled", flat=True).first()
    if enabled is None:
        enabled = default
    cache.set(cache_key, enabled, CACHE_SECONDS)
    return enabled

def get_active_story_blocks():
    return HomepageStoryBlock.objects.filter(is_active=True)

def get_active_brand_badges():
    return BrandBadge.objects.filter(is_active=True)
