from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from .services import add_product, get_existing_wishlist, get_or_create_wishlist, remove_product

class WishlistDetailView(TemplateView):
    template_name = "wishlist/detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist = get_existing_wishlist(self.request)
        context.update({"wishlist": wishlist, "wishlist_items": wishlist.items.select_related("product", "product__category").prefetch_related("product__variants", "product__images") if wishlist else [], "page_title": "Избранное — Airish Fox", "meta_description": "Ваши избранные образы Airish Fox."})
        return context

class WishlistAddView(View):
    http_method_names = ["post"]
    def post(self, request, product_id):
        add_product(request, product_id); messages.success(request, "Товар добавлен в избранное.")
        return redirect(request.META.get("HTTP_REFERER") or "wishlist:detail")

class WishlistRemoveView(View):
    http_method_names = ["post"]
    def post(self, request, product_id):
        remove_product(request, product_id); messages.success(request, "Товар удалён из избранного.")
        return redirect(request.META.get("HTTP_REFERER") or "wishlist:detail")

class WishlistToggleView(View):
    http_method_names = ["post"]
    def post(self, request, product_id):
        wishlist = get_or_create_wishlist(request)
        if wishlist.items.filter(product_id=product_id).exists():
            wishlist.items.filter(product_id=product_id).delete(); messages.success(request, "Товар удалён из избранного.")
        else:
            add_product(request, product_id); messages.success(request, "Товар добавлен в избранное.")
        return redirect(request.META.get("HTTP_REFERER") or "wishlist:detail")
