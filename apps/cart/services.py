"""Service layer for cart operations."""

from dataclasses import dataclass

from django.db import transaction

from apps.catalog.models import ProductVariant

from .models import Cart, CartItem


class CartError(Exception):
    """Expected cart operation error with a customer-friendly message."""


@dataclass
class CartOperationResult:
    cart: Cart
    item: CartItem | None = None
    message: str = ""


def _ensure_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_or_create_cart(request):
    """Return the active cart for the current user or anonymous session."""
    if request.user.is_authenticated:
        cart, _created = Cart.objects.get_or_create(user=request.user, status=Cart.Status.ACTIVE, defaults={"session_key": request.session.session_key})
        return cart

    session_key = _ensure_session_key(request)
    cart_id = request.session.get("cart_id")
    if cart_id:
        cart = Cart.objects.filter(pk=cart_id, user__isnull=True, status=Cart.Status.ACTIVE).first()
        if cart:
            return cart
    cart = Cart.objects.filter(session_key=session_key, user__isnull=True, status=Cart.Status.ACTIVE).first()
    if not cart:
        cart = Cart.objects.create(session_key=session_key, status=Cart.Status.ACTIVE)
    request.session["cart_id"] = cart.pk
    return cart


def _get_existing_cart(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user, status=Cart.Status.ACTIVE).first()
    cart_id = request.session.get("cart_id")
    if cart_id:
        cart = Cart.objects.filter(pk=cart_id, user__isnull=True, status=Cart.Status.ACTIVE).first()
        if cart:
            return cart
    session_key = request.session.session_key
    if not session_key:
        return None
    return Cart.objects.filter(session_key=session_key, user__isnull=True, status=Cart.Status.ACTIVE).first()


def _validate_variant_for_cart(variant, requested_quantity):
    if requested_quantity < 1:
        raise CartError("Количество должно быть не меньше 1.")
    if not variant.is_active:
        raise CartError("Этот вариант товара сейчас недоступен.")
    if not variant.product.is_active:
        raise CartError("Этот товар сейчас недоступен.")
    if variant.stock_quantity <= 0:
        raise CartError("Этого варианта сейчас нет в наличии.")
    if requested_quantity > variant.stock_quantity:
        raise CartError(f"На складе доступно только {variant.stock_quantity} шт.")


@transaction.atomic
def add_to_cart(request, variant_id, quantity=1):
    quantity = int(quantity or 1)
    variant = ProductVariant.objects.select_for_update().select_related("product").get(pk=variant_id)
    _validate_variant_for_cart(variant, quantity)
    cart = get_or_create_cart(request)
    item = CartItem.objects.select_for_update().filter(cart=cart, variant=variant).first()

    if item:
        new_quantity = item.quantity + quantity
        _validate_variant_for_cart(variant, new_quantity)
        item.quantity = new_quantity
        item.save(update_fields=["quantity", "updated_at"])
        return CartOperationResult(cart=cart, item=item, message="Количество товара в корзине обновлено.")

    item = CartItem.objects.create(cart=cart, variant=variant, quantity=quantity, unit_price_snapshot=variant.price)
    return CartOperationResult(cart=cart, item=item, message="Товар добавлен в корзину.")


@transaction.atomic
def update_cart_item(request, item_id, quantity):
    quantity = int(quantity or 1)
    cart = get_or_create_cart(request)
    item = CartItem.objects.select_for_update().select_related("variant", "variant__product").filter(cart=cart, pk=item_id).first()
    if not item:
        raise CartError("Позиция корзины не найдена.")
    _validate_variant_for_cart(item.variant, quantity)
    item.quantity = quantity
    item.save(update_fields=["quantity", "updated_at"])
    return CartOperationResult(cart=cart, item=item, message="Корзина обновлена.")


@transaction.atomic
def remove_cart_item(request, item_id):
    cart = get_or_create_cart(request)
    item = CartItem.objects.filter(cart=cart, pk=item_id).first()
    if not item:
        raise CartError("Позиция корзины не найдена.")
    item.delete()
    return CartOperationResult(cart=cart, message="Товар удалён из корзины.")


@transaction.atomic
def clear_cart(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    return CartOperationResult(cart=cart, message="Корзина очищена.")


@transaction.atomic
def merge_session_cart_into_user_cart(request, user):
    """Merge anonymous session cart into the active user cart after login."""
    session_key = request.session.session_key
    cart_id = request.session.get("cart_id")
    if not session_key and not cart_id:
        return None

    session_carts = Cart.objects.select_for_update().filter(user__isnull=True, status=Cart.Status.ACTIVE)
    if cart_id:
        session_carts = session_carts.filter(pk=cart_id)
    else:
        session_carts = session_carts.filter(session_key=session_key)
    session_cart = session_carts.prefetch_related("items__variant").first()
    if not session_cart:
        return None

    user_cart, _created = Cart.objects.select_for_update().get_or_create(
        user=user,
        status=Cart.Status.ACTIVE,
        defaults={"session_key": session_key},
    )

    for session_item in session_cart.items.select_related("variant", "variant__product"):
        variant = session_item.variant
        if not variant.is_active or not variant.product.is_active or variant.stock_quantity <= 0:
            continue
        quantity_to_merge = min(session_item.quantity, variant.stock_quantity)
        user_item = CartItem.objects.select_for_update().filter(cart=user_cart, variant=variant).first()
        if user_item:
            user_item.quantity = min(user_item.quantity + quantity_to_merge, variant.stock_quantity)
            user_item.save(update_fields=["quantity", "updated_at"])
        else:
            CartItem.objects.create(
                cart=user_cart,
                variant=variant,
                quantity=quantity_to_merge,
                unit_price_snapshot=session_item.unit_price_snapshot,
            )

    session_cart.status = Cart.Status.CONVERTED
    session_cart.save(update_fields=["status", "updated_at"])
    session_cart.items.all().delete()
    request.session.pop("cart_id", None)
    return user_cart


def get_cart_for_summary(request):
    """Return current active cart without creating a new cart."""
    return _get_existing_cart(request)
