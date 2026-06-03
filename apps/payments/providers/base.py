"""Payment provider abstraction."""


class PaymentProvider:
    provider_name: str

    def create_payment(self, order):
        raise NotImplementedError

    def parse_return(self, request):
        raise NotImplementedError

    def verify_notification(self, request) -> dict:
        raise NotImplementedError

    def handle_notification(self, webhook_event):
        raise NotImplementedError
