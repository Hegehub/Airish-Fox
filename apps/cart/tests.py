"""Tests for cart services, views and merge behavior."""

from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import Category, Product, ProductVariant

from .models import Cart, CartItem


class CartTestDataMixin:
    def setUp(self):
        self.category = Category.objects.create(name="Tops", slug="tops")
        self.product = Product.objects.create(
            name="Mint Top",
            slug="mint-top",
            category=self.category,
            short_description="Soft mint top",
            is_active=True,
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku="AF-MINT-TOP-S",
            size="S",
            color_name="Mint",
            color_hex="#B8F2D0",
            price=Decimal("100.00"),
            stock_quantity=5,
            is_active=True,
        )
        self.user = User.objects.create_user(username="cartfox", email="cart@example.com", password="StrongPass123")


class CartViewTests(CartTestDataMixin, TestCase):
    def test_cart_page_returns_200(self):
        response = self.client.get(reverse("cart:detail"))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_can_add_variant_to_cart(self):
        response = self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 2})
        self.assertRedirects(response, reverse("cart:detail"))
        cart = Cart.objects.get(user__isnull=True, status=Cart.Status.ACTIVE)
        self.assertEqual(cart.items.get().quantity, 2)

    def test_authenticated_user_can_add_variant_to_cart(self):
        self.client.login(username="cartfox", password="StrongPass123")
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        cart = Cart.objects.get(user=self.user, status=Cart.Status.ACTIVE)
        self.assertEqual(cart.items.get().variant, self.variant)

    def test_adding_same_variant_increments_quantity(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 2})
        self.assertEqual(CartItem.objects.get().quantity, 3)

    def test_cannot_add_inactive_variant(self):
        self.variant.is_active = False
        self.variant.save(update_fields=["is_active"])
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        self.assertFalse(CartItem.objects.exists())

    def test_cannot_add_product_with_inactive_product(self):
        self.product.is_active = False
        self.product.save(update_fields=["is_active"])
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        self.assertFalse(CartItem.objects.exists())

    def test_cannot_add_more_than_stock_quantity(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 6})
        self.assertFalse(CartItem.objects.exists())

    def test_can_update_cart_item_quantity(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        item = CartItem.objects.get()
        response = self.client.post(reverse("cart:update", kwargs={"item_id": item.id}), {"quantity": 4})
        self.assertRedirects(response, reverse("cart:detail"))
        item.refresh_from_db()
        self.assertEqual(item.quantity, 4)

    def test_cannot_update_quantity_above_stock(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        item = CartItem.objects.get()
        self.client.post(reverse("cart:update", kwargs={"item_id": item.id}), {"quantity": 8})
        item.refresh_from_db()
        self.assertEqual(item.quantity, 1)


    def test_cannot_update_another_cart_item(self):
        other_user = User.objects.create_user(username="othercart", email="othercart@example.com", password="StrongPass123")
        other_cart = Cart.objects.create(user=other_user, status=Cart.Status.ACTIVE)
        other_item = CartItem.objects.create(cart=other_cart, variant=self.variant, quantity=1, unit_price_snapshot=self.variant.price)
        self.client.login(username="cartfox", password="StrongPass123")
        self.client.post(reverse("cart:update", kwargs={"item_id": other_item.id}), {"quantity": 4})
        other_item.refresh_from_db()
        self.assertEqual(other_item.quantity, 1)

    def test_can_remove_item(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        item = CartItem.objects.get()
        self.client.post(reverse("cart:remove", kwargs={"item_id": item.id}))
        self.assertFalse(CartItem.objects.exists())

    def test_can_clear_cart(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        self.client.post(reverse("cart:clear"))
        self.assertFalse(CartItem.objects.exists())

    def test_subtotal_is_correct(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 3})
        cart = Cart.objects.get(status=Cart.Status.ACTIVE)
        self.assertEqual(cart.get_subtotal(), Decimal("300.00"))

    def test_cart_item_line_total_is_correct(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 2})
        self.assertEqual(CartItem.objects.get().get_line_total(), Decimal("200.00"))

    def test_guest_cart_merges_into_user_cart_after_login(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 2})
        response = self.client.post(reverse("accounts:login"), {"username": "cartfox", "password": "StrongPass123"})
        self.assertRedirects(response, reverse("accounts:dashboard"))
        user_cart = Cart.objects.get(user=self.user, status=Cart.Status.ACTIVE)
        self.assertEqual(user_cart.items.get(variant=self.variant).quantity, 2)
        self.assertTrue(Cart.objects.filter(user__isnull=True, status=Cart.Status.CONVERTED).exists())

    def test_merge_does_not_exceed_stock(self):
        user_cart = Cart.objects.create(user=self.user, status=Cart.Status.ACTIVE)
        CartItem.objects.create(cart=user_cart, variant=self.variant, quantity=4, unit_price_snapshot=self.variant.price)
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 3})
        self.client.post(reverse("accounts:login"), {"username": "cartfox", "password": "StrongPass123"})
        user_cart.refresh_from_db()
        self.assertEqual(user_cart.items.get(variant=self.variant).quantity, 5)

    def test_navbar_cart_count_context_works(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 2})
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.context["cart_items_count"], 2)
        self.assertContains(response, "cart-count-badge")

    def test_empty_cart_page_uses_mascot_without_emoji(self):
        response = self.client.get(reverse("cart:detail"))
        self.assertContains(response, "fox-mascot-idle.svg")
        self.assertNotContains(response, "\U0001f98a")
