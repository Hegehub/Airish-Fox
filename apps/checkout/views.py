"""Checkout views."""

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView

from apps.cart.services import get_or_create_cart
from apps.core.ratelimit import check_rate_limit

from .forms import CheckoutForm
from .services import CheckoutError, CheckoutService


class CheckoutView(FormView):
    template_name = "checkout/checkout.html"
    form_class = CheckoutForm

    def dispatch(self, request, *args, **kwargs):
        self.cart = get_or_create_cart(request)
        if self.cart.is_empty():
            messages.error(request, "Корзина пуста.")
            return redirect("cart:detail")
        if request.method == "POST" and check_rate_limit(request, "checkout").limited:
            messages.error(request, "Слишком много попыток оформления заказа. Попробуйте позже.")
            return HttpResponse("Too many checkout attempts.", status=429)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "cart": self.cart,
                "cart_items": self.cart.items.select_related("variant", "variant__product"),
                "subtotal": self.cart.get_subtotal(),
                "page_title": "Оформление заказа — Airish Fox",
                "meta_description": "Оформление заказа Airish Fox без онлайн-оплаты на этом этапе.",
            }
        )
        return context

    def form_valid(self, form):
        try:
            order = CheckoutService().create_order_from_cart(
                cart=self.cart,
                form_data=form.cleaned_data,
                user=self.request.user,
                request=self.request,
            )
        except CheckoutError as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)
        messages.success(self.request, "Заказ создан и ожидает оплаты.")
        return redirect(order.get_absolute_url())
