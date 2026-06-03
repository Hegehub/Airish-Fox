"""Admin for brand experience models."""
from django.contrib import admin
from .models import BrandBadge, BrandFeatureToggle, HomepageStoryBlock

@admin.register(BrandFeatureToggle)
class BrandFeatureToggleAdmin(admin.ModelAdmin):
    list_display = ("key", "name", "is_enabled", "updated_at")
    list_filter = ("is_enabled",)
    search_fields = ("key", "name", "description")
    fieldsets = (("Feature", {"fields": ("key", "name", "description", "is_enabled")}),)

@admin.register(HomepageStoryBlock)
class HomepageStoryBlockAdmin(admin.ModelAdmin):
    list_display = ("title", "mascot_state", "is_active", "sort_order")
    list_filter = ("is_active", "mascot_state")
    search_fields = ("title", "subtitle", "text")
    list_editable = ("is_active", "sort_order")
    fieldsets = (("Content", {"fields": ("title", "subtitle", "text", "image", "mascot_state")}), ("CTA", {"fields": ("cta_label", "cta_url")}), ("Status", {"fields": ("is_active", "sort_order")}))

@admin.register(BrandBadge)
class BrandBadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "label", "color_hex", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("name", "label", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active", "sort_order")
