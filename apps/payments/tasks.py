"""Payment background task placeholders."""

import logging

from celery import shared_task

logger = logging.getLogger("apps.payments")


@shared_task(bind=True, ignore_result=True)
def payment_reconciliation_placeholder(self):
    logger.info("Payment reconciliation placeholder task")
