from django.contrib import admin
from .models import Wishlist, WishlistItem
class WishlistItemInline(admin.TabularInline):
    model = WishlistItem; extra = 0; readonly_fields = ("product", "created_at")
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    inlines = (WishlistItemInline,)
    list_display = ("user", "session_key", "created_at", "updated_at")
    search_fields = ("user__username", "user__email", "session_key")
    readonly_fields = ("created_at", "updated_at")
@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("wishlist", "product", "created_at")
    search_fields = ("product__name", "wishlist__user__username", "wishlist__session_key")
