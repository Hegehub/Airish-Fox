"""Payment selectors."""

from .models import PaymentTransaction


def latest_transaction_for_order(order):
    return PaymentTransaction.objects.filter(order=order).order_by("-created_at").first()
