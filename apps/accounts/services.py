"""Service helpers for customer accounts."""


def set_default_shipping_address(address):
    """Ensure the selected address is the only default shipping address for its user."""
    if address.is_default_shipping and address.user_id:
        address.user.addresses.exclude(pk=address.pk).update(is_default_shipping=False)
