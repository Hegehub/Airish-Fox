"""Cart context processors."""

from .services import get_cart_for_summary


def cart_summary(request):
    """Expose a lightweight cart count and subtotal without creating carts."""
    if not hasattr(request, "session"):
        return {"cart_items_count": 0, "cart_subtotal": 0}
    cart = get_cart_for_summary(request)
    if not cart:
        return {"cart_items_count": 0, "cart_subtotal": 0}
    return {
        "cart_items_count": cart.get_items_count(),
        "cart_subtotal": cart.get_subtotal(),
    }
