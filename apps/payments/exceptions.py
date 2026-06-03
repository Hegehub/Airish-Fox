"""Payment exceptions."""


class PaymentError(Exception):
    """Base expected payment error."""


class PaymentConfigurationError(PaymentError):
    """Raised when provider configuration is incomplete."""


class PaymentProviderError(PaymentError):
    """Raised when the payment provider request fails."""


class PaymentSignatureError(PaymentError):
    """Raised when a provider signature is invalid."""
