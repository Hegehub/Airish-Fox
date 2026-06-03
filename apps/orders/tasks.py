"""Order email task placeholders."""

import logging

from celery import shared_task

logger = logging.getLogger("apps.orders")


@shared_task(bind=True, ignore_result=True)
def send_order_confirmation_email(self, order_id: int):
    logger.info("Order confirmation email placeholder", extra={"order_id": order_id})


@shared_task(bind=True, ignore_result=True)
def send_payment_success_email(self, order_id: int):
    logger.info("Payment success email placeholder", extra={"order_id": order_id})


@shared_task(bind=True, ignore_result=True)
def send_payment_failed_email(self, order_id: int):
    logger.info("Payment failed email placeholder", extra={"order_id": order_id})
