"""Admin for promotions."""

from django.contrib import admin

from .models import PromoCode


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_type", "value", "is_active", "used_count", "max_uses", "valid_from", "valid_until")
    list_filter = ("discount_type", "is_active")
    search_fields = ("code", "description")
