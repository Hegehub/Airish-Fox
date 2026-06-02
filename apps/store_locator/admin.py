"""Admin for physical Airish Fox stores."""

from django.contrib import admin

from .models import StoreLocation, StoreOpeningHour, StorePhoto


class StoreOpeningHourInline(admin.TabularInline):
    model = StoreOpeningHour
    extra = 7
    max_num = 7


class StorePhotoInline(admin.TabularInline):
    model = StorePhoto
    extra = 1


@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    inlines = (StoreOpeningHourInline, StorePhotoInline)
    list_display = ("name", "city", "pickup_available", "fitting_available", "is_main_store", "is_active", "sort_order", "updated_at")
    list_filter = ("city", "is_active", "pickup_available", "fitting_available", "is_main_store")
    search_fields = ("name", "city", "district", "street_address", "full_address")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active", "sort_order")
    fieldsets = (
        ("Basic", {"fields": ("name", "slug", "short_description", "description")}),
        ("Address", {"fields": ("country", "city", "district", "street_address", "full_address")}),
        ("Coordinates", {"fields": ("latitude", "longitude")}),
        ("Contacts", {"fields": ("phone", "email", "whatsapp_url", "telegram_url", "instagram_url")}),
        ("Map", {"fields": ("google_maps_place_url", "google_maps_embed_url")}),
        ("Store Options", {"fields": ("is_active", "is_main_store", "pickup_available", "fitting_available", "sort_order")}),
        ("Media", {"fields": ("image",)}),
        ("SEO", {"fields": ("seo_title", "seo_description")}),
    )


@admin.register(StoreOpeningHour)
class StoreOpeningHourAdmin(admin.ModelAdmin):
    list_display = ("store", "weekday", "opens_at", "closes_at", "is_closed", "note")
    list_filter = ("weekday", "is_closed", "store")


@admin.register(StorePhoto)
class StorePhotoAdmin(admin.ModelAdmin):
    list_display = ("store", "alt_text", "sort_order")
    list_filter = ("store",)
