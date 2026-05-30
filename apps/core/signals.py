from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import SiteSettings
from .utils import clear_site_settings_cache


@receiver([post_save, post_delete], sender=SiteSettings)
def invalidate_site_settings_cache(**kwargs):
    clear_site_settings_cache()
