"""Cart lifecycle task placeholders."""

import logging

from celery import shared_task

logger = logging.getLogger("apps.cart")


@shared_task(bind=True, ignore_result=True)
def abandoned_cart_placeholder(self):
    logger.info("Abandoned cart scan placeholder")
