from django.contrib import admin
from .models import DropWaitlistEntry, ProductDrop
@admin.register(ProductDrop)
class ProductDropAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "starts_at", "ends_at", "is_active", "show_countdown", "waitlist_enabled")
    list_filter = ("is_active", "show_countdown", "waitlist_enabled", "starts_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("products",)
    fieldsets = (("Basic", {"fields": ("name", "slug", "description", "hero_image", "products")}), ("Timing", {"fields": ("starts_at", "ends_at", "is_active", "show_countdown", "waitlist_enabled")}), ("SEO", {"fields": ("seo_title", "seo_description")}))
@admin.register(DropWaitlistEntry)
class DropWaitlistEntryAdmin(admin.ModelAdmin):
    list_display = ("drop", "email", "name", "user", "is_notified", "created_at")
    list_filter = ("is_notified", "drop", "created_at")
    search_fields = ("email", "name", "drop__name")
    readonly_fields = ("created_at",)
