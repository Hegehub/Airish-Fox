"""Admin for shipping methods."""

from django.contrib import admin

from .models import ShippingMethod


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "base_price", "is_active", "sort_order")
    list_editable = ("base_price", "is_active", "sort_order")
    prepopulated_fields = {"code": ("name",)}
    search_fields = ("name", "code", "description")
