"""Views for Airish Fox physical store pages."""

import json

from django.conf import settings
from django.views.generic import DetailView, ListView

from .models import StoreLocation


class StoreContextMixin:
    def get_common_context(self):
        active_stores = StoreLocation.objects.filter(is_active=True).prefetch_related("opening_hours", "photos")
        main_store = active_stores.filter(is_main_store=True).first() or active_stores.first()
        return {
            "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
            "google_maps_map_id": settings.GOOGLE_MAPS_MAP_ID,
            "google_maps_default_zoom": settings.GOOGLE_MAPS_DEFAULT_ZOOM,
            "main_store": main_store,
            "active_stores": active_stores,
        }


class StoreListView(StoreContextMixin, ListView):
    template_name = "store_locator/store_list.html"
    context_object_name = "stores"

    def get_queryset(self):
        return StoreLocation.objects.filter(is_active=True).prefetch_related("opening_hours", "photos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        common = self.get_common_context()
        context.update(common)
        context.update(
            {
                "page_title": "Магазин Airish Fox во Вьетнаме",
                "meta_description": "Физический магазин Airish Fox: адрес, часы работы, примерка, самовывоз и маршрут через Google Maps.",
                "canonical_url": self.request.build_absolute_uri(self.request.path),
                "og_title": "Visit Airish Fox",
                "og_description": "Заберите заказ в магазине или загляните на примерку во Вьетнаме.",
            }
        )
        if common["main_store"] and common["main_store"].image:
            context["og_image"] = self.request.build_absolute_uri(common["main_store"].image.url)
        return context


class StoreDetailView(StoreContextMixin, DetailView):
    template_name = "store_locator/store_detail.html"
    context_object_name = "store"

    def get_queryset(self):
        return StoreLocation.objects.filter(is_active=True).prefetch_related("opening_hours", "photos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store = self.object
        context.update(self.get_common_context())
        context.update(
            {
                "page_title": store.seo_title or f"{store.name} — Airish Fox",
                "meta_description": store.seo_description or store.short_description or f"Адрес, часы работы и маршрут к {store.name}.",
                "canonical_url": self.request.build_absolute_uri(store.get_absolute_url()),
                "og_title": store.seo_title or store.name,
                "og_description": store.seo_description or store.short_description or store.get_display_address(),
                "local_business_json": self.build_local_business_json(store),
            }
        )
        if store.image:
            context["og_image"] = self.request.build_absolute_uri(store.image.url)
        return context

    def build_local_business_json(self, store):
        if not store.name or not store.latitude or not store.longitude:
            return ""
        data = {
            "@context": "https://schema.org",
            "@type": "ClothingStore",
            "name": store.name,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": store.street_address,
                "addressLocality": store.city,
                "addressRegion": store.district,
                "addressCountry": store.country,
            },
            "geo": {"@type": "GeoCoordinates", "latitude": str(store.latitude), "longitude": str(store.longitude)},
            "url": self.request.build_absolute_uri(store.get_absolute_url()),
        }
        if store.phone:
            data["telephone"] = store.phone
        opening_hours = []
        for item in store.opening_hours.all():
            if item.is_closed or not item.opens_at or not item.closes_at:
                continue
            weekday = item.get_weekday_display()[:2]
            opening_hours.append(f"{weekday} {item.opens_at:%H:%M}-{item.closes_at:%H:%M}")
        if opening_hours:
            data["openingHours"] = opening_hours
        return json.dumps(data, ensure_ascii=False)
