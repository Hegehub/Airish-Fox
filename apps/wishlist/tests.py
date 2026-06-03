from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from apps.catalog.models import Category, Product, ProductVariant
from .models import Wishlist, WishlistItem

class WishlistTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Cat", slug="cat")
        self.product = Product.objects.create(name="Fox Tee", slug="fox-tee", category=self.category, short_description="Soft")
        ProductVariant.objects.create(product=self.product, sku="TEE-S", size="S", color_name="Mint", price=Decimal("10.00"), stock_quantity=2)
    def test_wishlist_page_returns_200(self):
        self.assertEqual(self.client.get(reverse("wishlist:detail")).status_code, 200)
    def test_guest_can_add_wishlist_item(self):
        self.client.post(reverse("wishlist:add", args=[self.product.id]))
        self.assertEqual(WishlistItem.objects.count(), 1)
    def test_user_can_add_wishlist_item(self):
        User.objects.create_user("fox", password="x")
        self.client.login(username="fox", password="x")
        self.client.post(reverse("wishlist:add", args=[self.product.id]))
        self.assertEqual(Wishlist.objects.get().user.username, "fox")
    def test_duplicate_does_not_create_duplicates(self):
        url = reverse("wishlist:add", args=[self.product.id])
        self.client.post(url); self.client.post(url)
        self.assertEqual(WishlistItem.objects.count(), 1)
    def test_remove_works(self):
        self.client.post(reverse("wishlist:add", args=[self.product.id]))
        self.client.post(reverse("wishlist:remove", args=[self.product.id]))
        self.assertEqual(WishlistItem.objects.count(), 0)
