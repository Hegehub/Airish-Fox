"""Admin configuration for customer accounts."""

from django.contrib import admin

from .models import Address, CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone",
        "preferred_size_top",
        "preferred_size_bottom",
        "preferred_fit",
        "favorite_mood",
        "marketing_consent",
        "updated_at",
    )
    search_fields = ("user__username", "user__email", "phone")
    list_filter = ("preferred_fit", "marketing_consent", "favorite_mood")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "phone", "city", "district", "is_default_shipping", "updated_at")
    search_fields = ("user__username", "user__email", "full_name", "phone", "city", "street_address")
    list_filter = ("country", "city", "is_default_shipping")
