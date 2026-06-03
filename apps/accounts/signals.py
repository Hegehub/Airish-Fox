"""Signals for automatic customer profile creation."""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomerProfile


@receiver(post_save, sender=User)
def ensure_customer_profile(sender, instance, created, **kwargs):
    """Create one customer profile for each user without duplicating profiles."""
    if created:
        CustomerProfile.objects.get_or_create(user=instance)
