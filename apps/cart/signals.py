"""Signals for cart lifecycle events."""

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .services import merge_session_cart_into_user_cart


@receiver(user_logged_in)
def merge_cart_after_login(sender, request, user, **kwargs):
    """Merge the guest cart into the user's active cart after successful login."""
    merge_session_cart_into_user_cart(request, user)
