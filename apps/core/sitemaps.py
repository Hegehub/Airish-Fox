"""SEO sitemap definitions for public Airish Fox pages."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.catalog.models import Category, Collection, MoodCollection, Product
from apps.drops.models import ProductDrop
from apps.store_locator.models import StoreLocation


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return [
            "core:home",
            "catalog:product_list",
            "catalog:new_arrivals",
            "catalog:collection_list",
            "store_locator:store_list",
            "drops:list",
            "style_quiz:start",
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_active=True).order_by("slug")

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Category.objects.filter(is_active=True).order_by("sort_order", "name")


class CollectionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Collection.objects.filter(is_active=True).order_by("sort_order", "name")

    def lastmod(self, obj):
        return obj.updated_at


class MoodSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.75

    def items(self):
        return MoodCollection.objects.filter(is_active=True).order_by("sort_order", "name")

    def lastmod(self, obj):
        return obj.updated_at


class StoreSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return StoreLocation.objects.filter(is_active=True).order_by("sort_order", "name")

    def lastmod(self, obj):
        return obj.updated_at


class DropSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return ProductDrop.objects.filter(is_active=True).order_by("starts_at", "name")

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {
    "static": StaticViewSitemap,
    "products": ProductSitemap,
    "categories": CategorySitemap,
    "collections": CollectionSitemap,
    "moods": MoodSitemap,
    "stores": StoreSitemap,
    "drops": DropSitemap,
}
