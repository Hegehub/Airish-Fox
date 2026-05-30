from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.catalog.models import Product


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return ['core:home', 'core:about', 'catalog:collection', 'catalog:new_arrivals', 'reviews:reviews', 'contacts:contacts']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True, available=True)

    def lastmod(self, obj):
        return obj.updated_at
