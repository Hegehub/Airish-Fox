"""Payment reconciliation placeholder for Antom/2C2P pending transactions."""

from datetime import timedelta
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.payments.models import PaymentTransaction

logger = logging.getLogger("apps.payments")


class Command(BaseCommand):
    help = "List stale pending Antom payment transactions for manual/provider reconciliation."

    def add_arguments(self, parser):
        parser.add_argument("--older-than-minutes", type=int, default=30)
        parser.add_argument("--dry-run", action="store_true", default=True)

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(minutes=options["older_than_minutes"])
        transactions = PaymentTransaction.objects.select_related("order").filter(
            status__in=[PaymentTransaction.Status.CREATED, PaymentTransaction.Status.PENDING, PaymentTransaction.Status.REDIRECTED],
            created_at__lte=cutoff,
        )
        count = transactions.count()
        self.stdout.write(f"Found {count} pending payment transaction(s) older than {options['older_than_minutes']} minutes.")
        for transaction in transactions.iterator():
            line = f"{transaction.payment_request_id} order={transaction.order.number} status={transaction.status} amount={transaction.amount} {transaction.currency}"
            logger.info("Payment reconciliation candidate", extra={"payment_request_id": transaction.payment_request_id, "order_number": transaction.order.number})
            self.stdout.write(line)
        self.stdout.write("Dry run only: provider status fetch is intentionally TODO until live Antom API response contracts are confirmed.")
