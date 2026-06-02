"""Checkout service layer."""

from decimal import Decimal

from django.db import transaction

from apps.cart.models import Cart
from apps.catalog.models import ProductVariant
from apps.orders.models import Order, OrderItem, OrderStatusHistory
from apps.promotions.models import PromoCode


class CheckoutError(Exception):
    """Expected checkout error with a customer-facing message."""


class CheckoutService:
    @transaction.atomic
    def create_order_from_cart(self, cart, form_data, user=None, request=None):
        cart = Cart.objects.select_for_update().prefetch_related("items__variant__product").get(pk=cart.pk)
        if cart.status != Cart.Status.ACTIVE:
            raise CheckoutError("Эта корзина уже не активна.")
        items = list(cart.items.select_related("variant", "variant__product"))
        if not items:
            raise CheckoutError("Корзина пуста.")

        subtotal = Decimal("0.00")
        snapshots = []
        for item in items:
            variant = ProductVariant.objects.select_for_update().select_related("product").get(pk=item.variant_id)
            if not variant.is_active or not variant.product.is_active:
                raise CheckoutError(f"Товар {variant.product.name} сейчас недоступен.")
            if variant.stock_quantity < item.quantity:
                raise CheckoutError(f"Недостаточно товара {variant.product.name}. Доступно {variant.stock_quantity} шт.")
            line_total = item.unit_price_snapshot * item.quantity
            subtotal += line_total
            snapshots.append((item, variant, line_total))

        shipping_method = form_data["shipping_method"]
        pickup_store = form_data.get("pickup_store") if shipping_method and shipping_method.is_store_pickup else None
        shipping_total = Decimal("0.00") if shipping_method and shipping_method.is_store_pickup else (shipping_method.get_price_for_order(None) if shipping_method else Decimal("0.00"))

        promo = None
        discount_total = Decimal("0.00")
        promo_code_value = form_data.get("promo_code")
        if promo_code_value:
            promo = PromoCode.objects.select_for_update().get(code__iexact=promo_code_value)
            if not promo.can_apply_to_amount(subtotal):
                raise CheckoutError("Промокод нельзя применить к этому заказу.")
            discount_total = promo.calculate_discount(subtotal)

        grand_total = max(subtotal - discount_total + shipping_total, Decimal("0.00"))
        order = Order.objects.create(
            user=user if user and user.is_authenticated else None,
            email=form_data["email"],
            phone=form_data["phone"],
            full_name=form_data["full_name"],
            shipping_country=form_data.get("shipping_country") or "Vietnam",
            shipping_city=(pickup_store.city if pickup_store else form_data.get("shipping_city")) or "",
            shipping_district=(pickup_store.district if pickup_store else form_data.get("shipping_district")) or "",
            shipping_street_address=(pickup_store.get_display_address() if pickup_store else form_data.get("shipping_street_address")) or "",
            shipping_postal_code=form_data.get("shipping_postal_code") or "",
            shipping_method=shipping_method,
            shipping_method_name=shipping_method.name if shipping_method else "",
            pickup_store=pickup_store,
            pickup_store_name=pickup_store.name if pickup_store else "",
            pickup_store_address=pickup_store.get_display_address() if pickup_store else "",
            status=Order.Status.DRAFT,
            payment_status=Order.PaymentStatus.UNPAID,
            subtotal=subtotal,
            discount_total=discount_total,
            shipping_total=shipping_total,
            grand_total=grand_total,
            promo_code=promo,
            promo_code_snapshot=promo.code if promo else "",
            is_gift=form_data.get("is_gift", False),
            gift_wrap=form_data.get("gift_wrap", False),
            gift_message=form_data.get("gift_message", "") if form_data.get("is_gift") else "",
            hide_price_in_package=form_data.get("hide_price_in_package", False),
            notes=form_data.get("notes", ""),
            customer_ip=self._get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "") if request else "",
        )

        for item, variant, line_total in snapshots:
            OrderItem.objects.create(
                order=order,
                product_id_snapshot=variant.product_id,
                variant_id_snapshot=variant.id,
                product_name=variant.product.name,
                variant_sku=variant.sku,
                size=variant.size,
                color_name=variant.color_name,
                color_hex=variant.color_hex,
                quantity=item.quantity,
                unit_price=item.unit_price_snapshot,
                line_total=line_total,
            )

        OrderStatusHistory.objects.create(order=order, old_status="", new_status=Order.Status.DRAFT, comment="Заказ создан из корзины.")
        order.mark_pending_payment()
        if promo:
            promo.used_count += 1
            promo.save(update_fields=["used_count", "updated_at"])
        cart.status = Cart.Status.CONVERTED
        cart.save(update_fields=["status", "updated_at"])
        if request:
            request.session.pop("cart_id", None)
            order_numbers = request.session.get("order_numbers", [])
            if order.number not in order_numbers:
                order_numbers.append(order.number)
            request.session["order_numbers"] = order_numbers
        return order

    def _get_client_ip(self, request):
        if not request:
            return None
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
