"""Admin for orders."""

from django.contrib import admin

from .models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = [field.name for field in OrderItem._meta.fields]


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    can_delete = False
    readonly_fields = [field.name for field in OrderStatusHistory._meta.fields]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline, OrderStatusHistoryInline)
    list_display = ("number", "email", "full_name", "status", "payment_status", "requires_manual_review", "grand_total", "currency", "created_at")
    list_filter = ("status", "payment_status", "requires_manual_review", "is_gift", "gift_wrap", "currency", "created_at")
    search_fields = ("number", "email", "phone", "full_name")
    readonly_fields = ("number", "created_at", "updated_at", "subtotal", "discount_total", "shipping_total", "grand_total")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_name", "variant_sku", "quantity", "unit_price", "line_total")
    search_fields = ("order__number", "product_name", "variant_sku")


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("order", "old_status", "new_status", "created_at")
    search_fields = ("order__number", "comment")
