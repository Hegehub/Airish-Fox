"""Payment service layer."""

from __future__ import annotations

import logging
from decimal import Decimal
from uuid import uuid4

from django.db import transaction
from django.utils import timezone

from apps.catalog.models import ProductVariant
from apps.orders.models import Order, OrderStatusHistory

from .exceptions import PaymentError
from .models import PaymentStatusHistory, PaymentTransaction

logger = logging.getLogger("payments")


def ensure_order_can_be_paid(order: Order):
    if order.payment_status == Order.PaymentStatus.PAID:
        raise PaymentError("Этот заказ нельзя оплатить повторно.")
    if not order.can_be_paid():
        raise PaymentError("Этот заказ сейчас нельзя оплатить.")
    if order.grand_total <= Decimal("0"):
        raise PaymentError("Сумма заказа должна быть больше нуля.")
    return True


def build_payment_request_id(order: Order) -> str:
    return f"PAY-{order.number}"


def get_or_create_payment_transaction(order: Order) -> PaymentTransaction:
    payment_request_id = build_payment_request_id(order)
    transaction_obj, created = PaymentTransaction.objects.get_or_create(
        payment_request_id=payment_request_id,
        defaults={
            "order": order,
            "amount": order.grand_total,
            "currency": order.currency,
            "idempotency_key": f"antom:{order.number}:{uuid4().hex}",
        },
    )
    if created:
        logger.info("Payment transaction created", extra={"payment_request_id": payment_request_id, "order": order.number})
    return transaction_obj


def create_payment_for_order(order: Order):
    ensure_order_can_be_paid(order)
    from .providers.antom_2c2p import Antom2C2PPaymentProvider

    return Antom2C2PPaymentProvider().create_payment(order)


def _record_payment_status(transaction_obj: PaymentTransaction, old_status: str, new_status: str, reason: str = "", payload=None):
    PaymentStatusHistory.objects.create(
        transaction=transaction_obj,
        old_status=old_status,
        new_status=new_status,
        reason=reason,
        raw_payload=payload or {},
    )


@transaction.atomic
def reduce_stock_for_paid_order(order: Order):
    """Reduce stock exactly once after a confirmed paid notification."""
    order = Order.objects.select_for_update().get(pk=order.pk)
    if order.payment_status == Order.PaymentStatus.PAID:
        logger.info("Duplicate stock reduction ignored", extra={"order": order.number})
        return False

    manual_review_reasons = []
    for item in order.items.all():
        if not item.variant_id_snapshot:
            manual_review_reasons.append(f"Missing variant snapshot for item {item.pk}")
            continue
        variant = ProductVariant.objects.select_for_update().filter(pk=item.variant_id_snapshot).first()
        if not variant:
            manual_review_reasons.append(f"Variant {item.variant_id_snapshot} not found")
            continue
        if variant.stock_quantity < item.quantity:
            manual_review_reasons.append(f"Insufficient stock for {variant.sku}: available {variant.stock_quantity}, required {item.quantity}")
            variant.stock_quantity = 0
            variant.save(update_fields=["stock_quantity", "updated_at"])
            continue
        variant.stock_quantity -= item.quantity
        variant.save(update_fields=["stock_quantity", "updated_at"])

    if manual_review_reasons:
        order.requires_manual_review = True
        order.manual_review_reason = "\n".join(manual_review_reasons)
        logger.error("Stock reduction requires manual review", extra={"order": order.number})
    return True


@transaction.atomic
def mark_transaction_paid(transaction_obj: PaymentTransaction, payload: dict):
    transaction_obj = PaymentTransaction.objects.select_for_update().select_related("order").get(pk=transaction_obj.pk)
    if transaction_obj.status == PaymentTransaction.Status.PAID:
        logger.info("Duplicate paid webhook ignored", extra={"payment_request_id": transaction_obj.payment_request_id})
        return transaction_obj

    old_status = transaction_obj.status
    order = transaction_obj.order
    reduce_stock_for_paid_order(order)
    order = Order.objects.select_for_update().get(pk=order.pk)
    old_order_status = order.status
    order.payment_status = Order.PaymentStatus.PAID
    order.status = Order.Status.PROCESSING
    order.save(update_fields=["payment_status", "status", "requires_manual_review", "manual_review_reason", "updated_at"])
    OrderStatusHistory.objects.create(order=order, old_status=old_order_status, new_status=order.status, comment="Оплата подтверждена Antom webhook.")

    transaction_obj.provider_payment_id = payload.get("paymentId") or payload.get("providerPaymentId", transaction_obj.provider_payment_id)
    transaction_obj.raw_response = payload
    transaction_obj.paid_at = timezone.now()
    transaction_obj.status = PaymentTransaction.Status.PAID
    transaction_obj.save(update_fields=["provider_payment_id", "raw_response", "paid_at", "status", "updated_at"])
    _record_payment_status(transaction_obj, old_status, transaction_obj.status, "paid webhook", payload)
    logger.info("Payment marked paid", extra={"payment_request_id": transaction_obj.payment_request_id, "order": order.number})
    return transaction_obj


@transaction.atomic
def mark_transaction_failed(transaction_obj: PaymentTransaction, payload: dict, reason: str = ""):
    transaction_obj = PaymentTransaction.objects.select_for_update().select_related("order").get(pk=transaction_obj.pk)
    if transaction_obj.status == PaymentTransaction.Status.PAID:
        logger.info("Ignoring failure for paid transaction", extra={"payment_request_id": transaction_obj.payment_request_id})
        return transaction_obj
    old_status = transaction_obj.status
    transaction_obj.status = PaymentTransaction.Status.FAILED
    transaction_obj.error_code = payload.get("result", {}).get("resultCode") or payload.get("paymentResultCode", "")
    transaction_obj.error_message = reason or payload.get("result", {}).get("resultMessage", "") or payload.get("paymentResultMessage", "")
    transaction_obj.raw_response = payload
    transaction_obj.failed_at = timezone.now()
    transaction_obj.save(update_fields=["status", "error_code", "error_message", "raw_response", "failed_at", "updated_at"])

    order = transaction_obj.order
    order.payment_status = Order.PaymentStatus.FAILED
    order.save(update_fields=["payment_status", "updated_at"])
    _record_payment_status(transaction_obj, old_status, transaction_obj.status, reason, payload)
    return transaction_obj
