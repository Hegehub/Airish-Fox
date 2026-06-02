"""Money formatting template filters."""

from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def money_vnd(value):
    try:
        amount = Decimal(value or 0)
    except (InvalidOperation, TypeError, ValueError):
        amount = Decimal("0")
    return f"{amount:,.0f} VND"
