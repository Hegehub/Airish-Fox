"""Admin configuration for carts."""

from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("unit_price_snapshot", "created_at", "updated_at")
    fields = ("variant", "quantity", "unit_price_snapshot", "created_at", "updated_at")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = (CartItemInline,)
    list_display = ("id", "user", "session_key", "status", "items_count", "subtotal", "updated_at")
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("user__email", "user__username", "session_key")
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Items")
    def items_count(self, obj):
        return obj.get_items_count()

    @admin.display(description="Subtotal")
    def subtotal(self, obj):
        return obj.get_subtotal()


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "variant", "quantity", "unit_price_snapshot", "line_total")
    search_fields = ("variant__sku", "variant__product__name")

    @admin.display(description="Line total")
    def line_total(self, obj):
        return obj.get_line_total()
