from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView

from apps.core.ratelimit import check_rate_limit

from .models import DropWaitlistEntry, ProductDrop


class DropListView(ListView):
    template_name = "drops/list.html"
    context_object_name = "drops"

    def get_queryset(self):
        return ProductDrop.objects.filter(is_active=True, ends_at__gte=timezone.now()).prefetch_related("products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_title": "Limited Drops — Airish Fox", "meta_description": "Лимитированные drops Airish Fox и waitlist."})
        return context


class DropDetailView(DetailView):
    template_name = "drops/detail.html"
    context_object_name = "drop"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return ProductDrop.objects.filter(is_active=True, ends_at__gte=timezone.now()).prefetch_related(
            "products", "products__variants", "products__images", "products__category"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drop = self.object
        context.update(
            {
                "products": drop.products.filter(is_active=True, variants__is_active=True).distinct(),
                "page_title": drop.seo_title or drop.name,
                "meta_description": drop.seo_description or drop.description,
            }
        )
        if drop.hero_image:
            context["og_image"] = self.request.build_absolute_uri(drop.hero_image.url)
        return context


class DropWaitlistView(View):
    http_method_names = ["post"]

    def post(self, request, slug):
        drop = get_object_or_404(ProductDrop, slug=slug, is_active=True, waitlist_enabled=True)
        if check_rate_limit(request, "waitlist").limited:
            messages.error(request, "Слишком много попыток записи в waitlist. Попробуйте позже.")
            return HttpResponse("Too many waitlist attempts.", status=429)
        if request.POST.get("website"):
            messages.success(request, "Спасибо. Если данные корректны, мы добавим вас в waitlist.")
            return redirect(drop.get_absolute_url())
        email = request.POST.get("email", "").strip().lower()
        name = request.POST.get("name", "").strip()
        if not email:
            messages.error(request, "Укажите email для waitlist.")
            return redirect(drop.get_absolute_url())
        if DropWaitlistEntry.objects.filter(drop=drop, email=email).exists():
            messages.error(request, "Этот email уже есть в waitlist.")
        else:
            DropWaitlistEntry.objects.create(drop=drop, email=email, name=name, user=request.user if request.user.is_authenticated else None)
            messages.success(request, "Вы в waitlist drop.")
        return redirect(drop.get_absolute_url())
