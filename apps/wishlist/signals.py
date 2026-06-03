from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .services import merge_session_wishlist_into_user

@receiver(user_logged_in)
def merge_wishlist_on_login(sender, request, user, **kwargs):
    merge_session_wishlist_into_user(request, user)
