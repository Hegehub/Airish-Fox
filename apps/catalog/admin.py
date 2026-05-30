from django.contrib import admin

from .models import Category, MoodCollection, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(MoodCollection)
class MoodCollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color_hex', 'is_active', 'sort_order')
    list_editable = ('color_hex', 'is_active', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'is_active', 'is_featured', 'is_new', 'is_fox_pick', 'sort_order', 'updated_at')
    list_filter = ('category', 'moods', 'is_active', 'is_featured', 'is_new', 'is_fox_pick', 'is_gift_ready', 'available')
    list_editable = ('price', 'available', 'is_active', 'is_featured', 'is_new', 'is_fox_pick', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description', 'description')
    filter_horizontal = ('moods',)
    inlines = [ProductImageInline]
    fieldsets = (
        ('Основное', {'fields': ('category', 'moods', 'name', 'slug', 'short_description', 'description', 'main_image')}),
        ('Характеристики', {'fields': ('price', 'sizes', 'color_name', 'color_hex', 'badge')}),
        ('Быстрый заказ', {'fields': ('whatsapp_message', 'telegram_message')}),
        ('Витрина', {'fields': ('available', 'is_active', 'is_featured', 'is_new', 'is_fox_pick', 'is_gift_ready', 'is_daily_pick', 'sort_order')}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category').prefetch_related('moods')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'sort_order')
    list_editable = ('sort_order',)
    search_fields = ('product__name', 'alt_text')
