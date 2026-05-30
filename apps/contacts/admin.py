from django.contrib import admin

from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'preferred_contact_method', 'phone', 'email', 'is_processed', 'created_at')
    list_filter = ('preferred_contact_method', 'is_processed', 'created_at')
    list_editable = ('is_processed',)
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at',)
