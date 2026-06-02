"""Payment views for Antom hosted flow."""

import json
import logging

from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.core.ratelimit import check_rate_limit
from apps.orders.models import Order

from .exceptions import PaymentError, PaymentSignatureError
from .models import PaymentTransaction
from .providers.antom_2c2p import Antom2C2PPaymentProvider
from .services import create_payment_for_order
from .webhooks import build_notification_response, create_webhook_event_from_request, process_antom_notification_event

logger = logging.getLogger("payments")


def user_can_access_order(request, order):
    if request.user.is_staff:
        return True
    if order.user_id:
        return request.user.is_authenticated and order.user_id == request.user.id
    return order.number in request.session.get("order_numbers", [])


class AntomCreatePaymentView(View):
    http_method_names = ["post"]

    def post(self, request, order_number):
        if check_rate_limit(request, "payment_create").limited:
            messages.error(request, "Слишком много попыток запуска оплаты. Попробуйте позже.")
            return HttpResponse("Too many payment attempts.", status=429)
        order = get_object_or_404(Order, number=order_number)
        if not user_can_access_order(request, order):
            raise Http404("Заказ не найден.")
        try:
            transaction = create_payment_for_order(order)
        except PaymentError as exc:
            messages.error(request, str(exc))
            return render(request, "payments/payment_failed.html", {"order": order, "error_message": str(exc)})
        if transaction.checkout_url:
            return redirect(transaction.checkout_url)
        return render(request, "payments/payment_redirect.html", {"order": order, "transaction": transaction})


class AntomReturnView(View):
    def get(self, request):
        transaction = Antom2C2PPaymentProvider().parse_return(request)
        context = {"transaction": transaction, "order": transaction.order if transaction else None}
        if not transaction:
            context["state"] = "unknown"
        elif transaction.status == PaymentTransaction.Status.PAID:
            context["state"] = "success"
        elif transaction.status in {PaymentTransaction.Status.FAILED, PaymentTransaction.Status.CANCELLED, PaymentTransaction.Status.EXPIRED}:
            context["state"] = "failed"
        else:
            context["state"] = "pending"
        return render(request, "payments/payment_return.html", context)


@method_decorator(csrf_exempt, name="dispatch")
class AntomNotifyView(View):
    http_method_names = ["post"]

    def post(self, request):
        provider = Antom2C2PPaymentProvider()
        try:
            payload = provider.verify_notification(request)
        except PaymentSignatureError as exc:
            event = create_webhook_event_from_request(request, signature_valid=False)
            event.processing_error = str(exc)
            event.save(update_fields=["processing_error"])
            logger.warning("Webhook invalid signature", extra={"event_id": event.pk})
            return JsonResponse(build_notification_response(False, "invalid signature"), status=400)
        except json.JSONDecodeError as exc:
            event = create_webhook_event_from_request(request, signature_valid=False, payload={})
            event.processing_error = f"Invalid JSON: {exc}"
            event.save(update_fields=["processing_error"])
            return JsonResponse(build_notification_response(False, "invalid json"), status=400)
        except Exception as exc:
            event = create_webhook_event_from_request(request, signature_valid=False)
            event.processing_error = str(exc)
            event.save(update_fields=["processing_error"])
            logger.warning("Webhook invalid signature", extra={"event_id": event.pk})
            return JsonResponse(build_notification_response(False, "invalid signature"), status=400)

        event = create_webhook_event_from_request(request, signature_valid=True, payload=payload)
        logger.info("Webhook received", extra={"payment_request_id": event.payment_request_id})
        process_antom_notification_event(event)
        if event.processing_error:
            return JsonResponse(build_notification_response(False, event.processing_error), status=202)
        return JsonResponse(build_notification_response(True))
