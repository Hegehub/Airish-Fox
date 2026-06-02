"""Tests for catalog models, views and components."""

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Category, Collection, MoodCollection, Product, ProductVariant


class CatalogTestDataMixin:
    def setUp(self):
        self.category = Category.objects.create(name="Dresses", slug="dresses", description="Soft dresses")
        self.collection = Collection.objects.create(name="Summer Drop", slug="summer-drop", description="Summer capsule")
        self.mood = MoodCollection.objects.create(name="Mint Mood", slug="mint-mood", description="Fresh mint mood")
        self.product = Product.objects.create(
            name="Mint Dress",
            slug="mint-dress",
            category=self.category,
            short_description="Лёгкое платье Airish Fox",
            description="Soft boutique dress.",
            is_active=True,
            is_new=True,
            is_featured=True,
            is_fox_pick=True,
        )
        self.product.collections.add(self.collection)
        self.product.moods.add(self.mood)
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku="AF-MINT-DRESS-S",
            size="S",
            color_name="Mint",
            color_hex="#B8F2D0",
            price=Decimal("1200.00"),
            stock_quantity=3,
        )


class CatalogModelTests(CatalogTestDataMixin, TestCase):
    def test_category_get_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(), f"{reverse('catalog:product_list')}?category=dresses")

    def test_product_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), reverse("catalog:product_detail", kwargs={"slug": "mint-dress"}))

    def test_variant_is_in_stock(self):
        self.assertTrue(self.variant.is_in_stock())

    def test_variant_can_purchase(self):
        self.assertTrue(self.variant.can_purchase(2))
        self.assertFalse(self.variant.can_purchase(4))

    def test_product_get_min_price(self):
        ProductVariant.objects.create(
            product=self.product,
            sku="AF-MINT-DRESS-M",
            size="M",
            color_name="Mint",
            price=Decimal("990.00"),
            stock_quantity=1,
        )
        self.assertEqual(self.product.get_min_price(), Decimal("990.00"))

    def test_product_is_available(self):
        self.assertTrue(self.product.is_available())

    def test_product_without_stock_is_unavailable_but_exists(self):
        self.variant.stock_quantity = 0
        self.variant.save(update_fields=["stock_quantity"])
        self.assertFalse(self.product.is_available())
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    def test_product_can_be_created_with_variant(self):
        product = Product.objects.create(
            name="Orange Shirt",
            slug="orange-shirt",
            category=self.category,
            short_description="Bright shirt",
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="AF-ORANGE-SHIRT-M",
            size="M",
            color_name="Orange",
            color_hex="#F7931A",
            price=Decimal("800.00"),
            stock_quantity=5,
        )
        self.assertEqual(product.variants.get(), variant)


class CatalogViewTests(CatalogTestDataMixin, TestCase):
    def test_catalog_returns_200(self):
        response = self.client.get(reverse("catalog:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_returns_200(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корзина скоро")

    def test_inactive_product_returns_404(self):
        self.product.is_active = False
        self.product.save(update_fields=["is_active"])
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_new_arrivals_returns_200(self):
        response = self.client.get(reverse("catalog:new_arrivals"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_category_filter_works(self):
        response = self.client.get(reverse("catalog:product_list"), {"category": self.category.slug})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["products"]), [self.product])

    def test_mood_filter_works(self):
        response = self.client.get(reverse("catalog:product_list"), {"mood": self.mood.slug})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["products"]), [self.product])

    def test_collection_filter_works(self):
        response = self.client.get(reverse("catalog:product_list"), {"collection": self.collection.slug})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["products"]), [self.product])

    def test_collection_detail_returns_200(self):
        response = self.client.get(self.collection.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_mood_detail_returns_200(self):
        response = self.client.get(self.mood.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_empty_state_uses_mascot_without_emoji(self):
        self.product.delete()
        response = self.client.get(reverse("catalog:product_list"))
        self.assertContains(response, "fox-mascot-idle.svg")
        self.assertNotContains(response, "\U0001f98a")

class MoodShoppingTests(TestCase):
    def test_mood_filter_works_and_empty_state_renders(self):
        mood = MoodCollection.objects.create(name="Soft Morning", slug="soft-morning", is_active=True)
        response = self.client.get(reverse("catalog:product_list"), {"mood": mood.slug})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Лисичка пока не нашла товары")

class CatalogSeoTests(CatalogTestDataMixin, TestCase):
    def test_product_detail_contains_schema_org_product(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertContains(response, '"@type": "Product"')
        self.assertContains(response, '"priceCurrency": "VND"')
