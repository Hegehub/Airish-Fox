from django.contrib import admin

from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'preferred_contact_method', 'phone', 'email', 'is_processed', 'created_at')
    list_filter = ('preferred_contact_method', 'is_processed', 'created_at', 'product')
    list_editable = ('is_processed',)
    search_fields = ('name', 'phone', 'email', 'message', 'admin_comment', 'product__name')
    readonly_fields = ('created_at', 'source_page', 'user_agent', 'ip_address', 'honeypot')
    fieldsets = (
        ('Заявка', {'fields': ('name', 'product', 'phone', 'email', 'preferred_contact_method', 'message', 'is_processed')}),
        ('Служебное', {'fields': ('source_page', 'user_agent', 'ip_address', 'honeypot', 'created_at')}),
        ('Админ', {'fields': ('admin_comment',)}),
    )
