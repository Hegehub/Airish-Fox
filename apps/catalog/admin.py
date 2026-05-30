from django.contrib import admin

from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'sizes', 'color_name', 'is_active', 'is_featured', 'is_new', 'updated_at')
    list_filter = ('category', 'is_active', 'is_featured', 'is_new', 'color_name')
    list_editable = ('price', 'is_active', 'is_featured', 'is_new')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description', 'description')
    inlines = [ProductImageInline]
    fieldsets = (
        ('Основное', {'fields': ('category', 'name', 'slug', 'short_description', 'description', 'main_image')}),
        ('Характеристики', {'fields': ('price', 'sizes', 'color_name', 'color_hex')}),
        ('Витрина', {'fields': ('is_active', 'is_featured', 'is_new')}),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'sort_order')
    list_editable = ('sort_order',)
    search_fields = ('product__name', 'alt_text')
