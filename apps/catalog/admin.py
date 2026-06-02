"""Django admin configuration for the Airish Fox catalog."""

from django.contrib import admin

from .models import Category, Collection, MoodCollection, Product, ProductImage, ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "sort_order", "updated_at")
    list_editable = ("is_active", "sort_order")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "sort_order", "updated_at")
    list_editable = ("is_active", "sort_order")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(MoodCollection)
class MoodCollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color_hex", "is_active", "sort_order", "updated_at")
    list_editable = ("color_hex", "is_active", "sort_order")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = (
        "sku",
        "size",
        "color_name",
        "color_hex",
        "price",
        "compare_at_price",
        "stock_quantity",
        "is_active",
        "sort_order",
    )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("variant", "image", "alt_text", "sort_order")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductVariantInline, ProductImageInline)
    list_display = (
        "name",
        "category",
        "display_min_price",
        "display_total_stock",
        "is_active",
        "is_featured",
        "is_new",
        "is_fox_pick",
        "is_gift_ready",
        "updated_at",
    )
    list_filter = (
        "category",
        "collections",
        "moods",
        "is_active",
        "is_featured",
        "is_new",
        "is_fox_pick",
        "is_gift_ready",
    )
    list_editable = ("is_active", "is_featured", "is_new", "is_fox_pick", "is_gift_ready")
    search_fields = ("name", "short_description", "description", "variants__sku")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("collections", "moods")
    fieldsets = (
        ("Основное", {"fields": ("name", "slug", "category", "collections", "moods")}),
        ("Описание", {"fields": ("short_description", "description", "material", "care_instructions")}),
        ("Брендовые признаки", {"fields": ("badge", "is_fox_pick", "is_gift_ready")}),
        ("SEO", {"fields": ("seo_title", "seo_description")}),
        ("Статусы", {"fields": ("is_active", "is_featured", "is_new")}),
    )

    @admin.display(description="Мин. цена")
    def display_min_price(self, obj):
        return obj.get_min_price() or "—"

    @admin.display(description="Остаток")
    def display_total_stock(self, obj):
        return sum(variant.stock_quantity for variant in obj.get_active_variants())


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("sku", "product", "size", "color_name", "price", "stock_quantity", "is_active", "updated_at")
    list_filter = ("is_active", "size", "color_name")
    search_fields = ("sku", "product__name", "size", "color_name")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "variant", "alt_text", "sort_order", "created_at")
    list_filter = ("product",)
    search_fields = ("product__name", "variant__sku", "alt_text")
