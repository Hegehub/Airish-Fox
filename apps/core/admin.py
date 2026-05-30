from django.contrib import admin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'email', 'phone', 'updated_at')
    fieldsets = (
        ('Бренд', {'fields': ('site_name', 'slogan', 'short_description', 'hero_image')}),
        ('Контакты', {'fields': ('telegram_url', 'whatsapp_url', 'instagram_url', 'email', 'phone')}),
    )
