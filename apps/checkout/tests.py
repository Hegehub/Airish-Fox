"""Checkout tests."""

from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.cart.models import Cart, CartItem
from apps.catalog.models import Category, Product, ProductVariant
from apps.orders.models import Order
from apps.promotions.models import PromoCode
from apps.shipping.models import ShippingMethod


class CheckoutTestDataMixin:
    def setUp(self):
        self.category = Category.objects.create(name="Dresses", slug="checkout-dresses")
        self.product = Product.objects.create(name="Checkout Dress", slug="checkout-dress", category=self.category, short_description="Dress")
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku="AF-CHECKOUT-DRESS-S",
            size="S",
            color_name="Mint",
            price=Decimal("1000.00"),
            stock_quantity=5,
        )
        self.shipping = ShippingMethod.objects.create(name="Standard delivery", code="standard-delivery", base_price=Decimal("100.00"))
        self.user = User.objects.create_user(username="checkoutfox", email="checkout@example.com", password="StrongPass123")

    def create_cart(self, user=None, quantity=2):
        cart = Cart.objects.create(user=user, status=Cart.Status.ACTIVE)
        CartItem.objects.create(cart=cart, variant=self.variant, quantity=quantity, unit_price_snapshot=self.variant.price)
        return cart

    def checkout_data(self, **overrides):
        data = {
            "full_name": "Airish Fox",
            "email": "customer@example.com",
            "phone": "+84900000000",
            "shipping_country": "Vietnam",
            "shipping_city": "Ho Chi Minh City",
            "shipping_district": "District 1",
            "shipping_street_address": "1 Boutique Street",
            "shipping_postal_code": "700000",
            "shipping_method": self.shipping.id,
            "promo_code": "",
            "notes": "",
        }
        data.update(overrides)
        return data


class CheckoutTests(CheckoutTestDataMixin, TestCase):
    def test_empty_cart_redirects_to_cart(self):
        response = self.client.get(reverse("checkout:checkout"))
        self.assertRedirects(response, reverse("cart:detail"))

    def test_checkout_page_opens_with_active_cart(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        response = self.client.get(reverse("checkout:checkout"))
        self.assertEqual(response.status_code, 200)

    def test_order_is_created_from_cart(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 2})
        response = self.client.post(reverse("checkout:checkout"), self.checkout_data())
        order = Order.objects.get()
        self.assertRedirects(response, order.get_absolute_url())
        self.assertEqual(order.status, Order.Status.PENDING_PAYMENT)

    def test_order_items_snapshot_created(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 2})
        self.client.post(reverse("checkout:checkout"), self.checkout_data())
        item = Order.objects.get().items.get()
        self.assertEqual(item.product_name, self.product.name)
        self.assertEqual(item.variant_sku, self.variant.sku)
        self.assertEqual(item.quantity, 2)

    def test_subtotal_shipping_promo_and_grand_total_calculated(self):
        promo = PromoCode.objects.create(code="MINT10", discount_type=PromoCode.DiscountType.PERCENT, value=Decimal("10"))
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 2})
        self.client.post(reverse("checkout:checkout"), self.checkout_data(promo_code=promo.code))
        order = Order.objects.get()
        self.assertEqual(order.subtotal, Decimal("2000.00"))
        self.assertEqual(order.discount_total, Decimal("200.00"))
        self.assertEqual(order.shipping_total, Decimal("100.00"))
        self.assertEqual(order.grand_total, Decimal("1900.00"))

    def test_cart_status_becomes_converted(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        self.client.post(reverse("checkout:checkout"), self.checkout_data())
        self.assertEqual(Cart.objects.get().status, Cart.Status.CONVERTED)

    def test_stock_is_not_reduced_on_order_creation(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 2})
        self.client.post(reverse("checkout:checkout"), self.checkout_data())
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 5)

    def test_guest_order_access_works_via_session(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        self.client.post(reverse("checkout:checkout"), self.checkout_data())
        order = Order.objects.get()
        response = self.client.get(order.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order.number)

    def test_authenticated_user_sees_order_in_history(self):
        self.client.login(username="checkoutfox", password="StrongPass123")
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        self.client.post(reverse("checkout:checkout"), self.checkout_data(email="checkout@example.com"))
        response = self.client.get(reverse("orders:history"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, Order.objects.get().number)


    def test_gift_mode_saves_to_order(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        self.client.post(reverse("checkout:checkout"), self.checkout_data(is_gift="on", gift_wrap="on", gift_message="Для любимой лисички", hide_price_in_package="on"))
        order = Order.objects.get()
        self.assertTrue(order.is_gift)
        self.assertTrue(order.gift_wrap)
        self.assertEqual(order.gift_message, "Для любимой лисички")
        self.assertTrue(order.hide_price_in_package)

    def test_gift_message_max_length_validates(self):
        self.client.post(reverse("cart:add"), {"variant_id": self.variant.id, "quantity": 1})
        response = self.client.post(reverse("checkout:checkout"), self.checkout_data(is_gift="on", gift_message="x" * 501))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Order.objects.exists())
