from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'is_active', 'created_at')
    list_filter = ('rating', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('customer_name', 'text')
