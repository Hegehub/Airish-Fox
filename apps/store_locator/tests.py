"""Tests for store locator pages and models."""

from datetime import time
from decimal import Decimal

from django.contrib import admin
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.orders.models import Order
from apps.shipping.models import ShippingMethod

from .models import StoreLocation, StoreOpeningHour


class StoreLocatorTests(TestCase):
    def setUp(self):
        self.store = StoreLocation.objects.create(
            name="Airish Fox Saigon",
            slug="airish-fox-saigon",
            short_description="Mint boutique in Vietnam",
            country="Vietnam",
            city="Ho Chi Minh City",
            district="District 1",
            street_address="1 Fox Street",
            latitude=Decimal("10.7769000"),
            longitude=Decimal("106.7009000"),
            google_maps_place_url="https://maps.google.com/?q=Airish+Fox",
            is_main_store=True,
        )
        StoreOpeningHour.objects.create(store=self.store, weekday=2, opens_at=time(10, 0), closes_at=time(20, 0))
        StoreOpeningHour.objects.create(store=self.store, weekday=0, opens_at=time(10, 0), closes_at=time(20, 0))
        self.inactive_store = StoreLocation.objects.create(
            name="Hidden Fox",
            slug="hidden-fox",
            city="Hanoi",
            street_address="Hidden",
            latitude=Decimal("21.0285000"),
            longitude=Decimal("105.8542000"),
            is_active=False,
        )

    @override_settings(GOOGLE_MAPS_API_KEY="")
    def test_store_list_page_returns_200(self):
        response = self.client.get(reverse("store_locator:store_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visit Airish Fox")

    def test_store_detail_page_returns_200(self):
        response = self.client.get(self.store.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.store.name)

    def test_inactive_store_not_in_list(self):
        response = self.client.get(reverse("store_locator:store_list"))
        self.assertContains(response, self.store.name)
        self.assertNotContains(response, self.inactive_store.name)

    def test_store_get_absolute_url(self):
        self.assertEqual(self.store.get_absolute_url(), reverse("store_locator:store_detail", kwargs={"slug": self.store.slug}))

    def test_get_directions_url_returns_google_maps_url(self):
        url = self.store.get_directions_url()
        self.assertTrue(url.startswith("https://www.google.com/maps/dir/"))
        self.assertIn("10.7769000", url)

    @override_settings(GOOGLE_MAPS_API_KEY="")
    def test_page_works_without_google_maps_api_key_and_shows_fallback(self):
        response = self.client.get(self.store.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "store-map-fallback")

    def test_admin_registration_smoke(self):
        self.assertIn(StoreLocation, admin.site._registry)
        self.assertIn(StoreOpeningHour, admin.site._registry)

    def test_opening_hours_ordering(self):
        weekdays = list(self.store.opening_hours.values_list("weekday", flat=True))
        self.assertEqual(weekdays, [0, 2])

    def test_store_location_can_be_used_as_pickup_store(self):
        shipping = ShippingMethod.objects.create(name="Store pickup", code="store-pickup", base_price=Decimal("0.00"))
        order = Order.objects.create(
            email="fox@example.com",
            phone="1",
            full_name="Fox",
            shipping_city=self.store.city,
            shipping_street_address=self.store.get_display_address(),
            shipping_method=shipping,
            shipping_method_name=shipping.name,
            pickup_store=self.store,
            pickup_store_name=self.store.name,
            pickup_store_address=self.store.get_display_address(),
        )
        self.assertEqual(order.pickup_store, self.store)

    def test_store_detail_includes_local_business_schema(self):
        response = self.client.get(self.store.get_absolute_url())
        self.assertContains(response, '"@type": "ClothingStore"')
        self.assertContains(response, self.store.street_address)
