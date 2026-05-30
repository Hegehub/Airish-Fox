from django.contrib import admin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'primary_contact_method', 'email', 'phone', 'mascot_enabled', 'updated_at')
    fieldsets = (
        ('Brand', {'fields': ('site_name', 'slogan', 'short_description', 'brand_note')}),
        ('Hero', {'fields': ('hero_title', 'hero_subtitle', 'hero_cta_primary_label', 'hero_cta_secondary_label', 'hero_image')}),
        ('Contacts', {'fields': ('primary_contact_method', 'telegram_url', 'whatsapp_url', 'instagram_url', 'email', 'phone')}),
        ('Mascot', {'fields': ('mascot_enabled', 'mascot_provider', 'mascot_static_image', 'mascot_animation_url')}),
        ('SEO', {'fields': ('seo_title', 'seo_description', 'og_image')}),
        ('Footer', {'fields': ('footer_text',)}),
    )
