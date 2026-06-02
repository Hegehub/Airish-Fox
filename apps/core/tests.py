"""Foundation tests for the core Airish Fox app."""

from pathlib import Path

from django.conf import settings
from django.test import TestCase
from django.urls import reverse


class CorePageTests(TestCase):
    def test_home_page_returns_200(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Airish Fox")

    def test_healthcheck_returns_200(self):
        response = self.client.get(reverse("core:healthcheck"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_robots_txt_returns_200(self):
        response = self.client.get(reverse("core:robots_txt"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/plain", response["Content-Type"])
        self.assertContains(response, "User-agent: *")

    def test_base_template_renders(self):
        response = self.client.get(reverse("core:home"))
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, "site.css")

    def test_brand_svg_files_exist(self):
        brand_dir = Path(settings.BASE_DIR) / "static" / "images" / "brand"
        for filename in ["fox-logo.svg", "fox-mark.svg", "fox-mascot-idle.svg"]:
            with self.subTest(filename=filename):
                self.assertTrue((brand_dir / filename).is_file())

    def test_favicon_svg_exists(self):
        favicon = Path(settings.BASE_DIR) / "static" / "images" / "brand" / "fox-favicon.svg"
        self.assertTrue(favicon.is_file())

class BrandExperienceHomeTests(TestCase):
    def test_home_shows_mood_collection(self):
        from apps.catalog.models import MoodCollection
        MoodCollection.objects.create(name="Mint Mood", slug="mint-mood", is_active=True)
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Mint Mood")

    def test_home_shows_only_in_stock_fox_pick(self):
        from decimal import Decimal
        from apps.catalog.models import Category, Product, ProductVariant
        category = Category.objects.create(name="Fox", slug="fox-home")
        product = Product.objects.create(name="Fox Pick Dress", slug="fox-pick-dress", category=category, short_description="Pick", is_fox_pick=True)
        ProductVariant.objects.create(product=product, sku="PICK-S", size="S", color_name="Mint", price=Decimal("10.00"), stock_quantity=1)
        out = Product.objects.create(name="Out Pick", slug="out-pick", category=category, short_description="Out", is_fox_pick=True)
        ProductVariant.objects.create(product=out, sku="OUT-S", size="S", color_name="Mint", price=Decimal("10.00"), stock_quantity=0)
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Fox Pick Dress")
        self.assertNotContains(response, "Out Pick")

class ProductionHardeningTests(TestCase):
    def test_sitemap_returns_200(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)

    def test_robots_lists_sitemap_and_private_paths(self):
        response = self.client.get(reverse("core:robots_txt"))
        content = response.content.decode()
        self.assertIn("Sitemap:", content)
        self.assertIn("Disallow: /cart/", content)
        self.assertIn("Disallow: /checkout/", content)
        self.assertIn("Disallow: /payments/", content)

    def test_home_has_canonical_seo_when_provided_by_base_context(self):
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "twitter:card")
        self.assertContains(response, "og:site_name")

    def test_skip_link_is_present(self):
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Перейти к содержимому")
