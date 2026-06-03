"""Cart views."""

from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import TemplateView

from apps.catalog.models import ProductImage, ProductVariant

from .models import CartItem
from .services import CartError, add_to_cart, clear_cart, get_or_create_cart, remove_cart_item, update_cart_item


def _redirect_back(request):
    referer = request.META.get("HTTP_REFERER")
    if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts={request.get_host()}):
        return redirect(referer)
    return redirect("cart:detail")


class CartDetailView(TemplateView):
    template_name = "cart/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        cart_items = (
            cart.items.select_related("variant", "variant__product", "variant__product__category")
            .prefetch_related(Prefetch("variant__product__images", queryset=ProductImage.objects.order_by("sort_order", "id")))
            .all()
        )
        context.update(
            {
                "cart": cart,
                "cart_items": cart_items,
                "subtotal": cart.get_subtotal(),
                "items_count": cart.get_items_count(),
                "page_title": "Корзина — Airish Fox",
                "meta_description": "Корзина Airish Fox с выбранными товарами и вариантами.",
            }
        )
        return context


class AddToCartView(View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        variant_id = request.POST.get("variant_id")
        quantity = request.POST.get("quantity", 1)
        try:
            result = add_to_cart(request, variant_id=variant_id, quantity=quantity)
        except ProductVariant.DoesNotExist:
            messages.error(request, "Выбранный вариант товара не найден.")
            return _redirect_back(request)
        except (CartError, ValueError, TypeError) as exc:
            messages.error(request, str(exc) or "Не удалось добавить товар в корзину.")
            return _redirect_back(request)
        messages.success(request, result.message)
        return redirect("cart:detail")


class UpdateCartItemView(View):
    http_method_names = ["post"]

    def post(self, request, item_id, *args, **kwargs):
        try:
            result = update_cart_item(request, item_id=item_id, quantity=request.POST.get("quantity", 1))
        except (CartError, ValueError, TypeError) as exc:
            messages.error(request, str(exc) or "Не удалось обновить корзину.")
        else:
            messages.success(request, result.message)
        return redirect("cart:detail")


class RemoveCartItemView(View):
    http_method_names = ["post"]

    def post(self, request, item_id, *args, **kwargs):
        try:
            result = remove_cart_item(request, item_id=item_id)
        except CartError as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, result.message)
        return redirect("cart:detail")


class ClearCartView(View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        result = clear_cart(request)
        messages.success(request, result.message)
        return redirect("cart:detail")
