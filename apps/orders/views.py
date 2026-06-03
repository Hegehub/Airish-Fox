"""Order views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import DetailView, ListView

from .models import Order


class OrderAccessMixin:
    model = Order
    slug_field = "number"
    slug_url_kwarg = "number"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.prefetch_related("items", "status_history").select_related("shipping_method", "promo_code", "user")

    def get_object(self, queryset=None):
        order = super().get_object(queryset)
        if self.request.user.is_authenticated and order.user_id == self.request.user.id:
            return order
        if not self.request.user.is_authenticated and order.number in self.request.session.get("order_numbers", []):
            return order
        raise Http404("Заказ не найден.")


class OrderDetailView(OrderAccessMixin, DetailView):
    template_name = "orders/order_detail.html"

    def get_template_names(self):
        if self.object.status == Order.Status.PENDING_PAYMENT:
            return ["orders/order_pending_payment.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_title": f"Заказ {self.object.number} — Airish Fox", "meta_description": "Детали заказа Airish Fox."})
        return context


class OrderHistoryView(LoginRequiredMixin, ListView):
    template_name = "orders/order_history.html"
    context_object_name = "orders"

    def get_queryset(self):
        return self.request.user.orders.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_title": "Мои заказы — Airish Fox", "meta_description": "История заказов Airish Fox."})
        return context
