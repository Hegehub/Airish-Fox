"""Views for the Airish Fox foundation pages."""

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from apps.catalog.models import MoodCollection
from apps.brand.services import get_active_story_blocks, is_feature_enabled
from apps.catalog.views import active_product_queryset


class HomeView(TemplateView):
    """Render the public landing page with catalog teasers."""

    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = active_product_queryset()
        context.update(
            {
                "featured_products": products.filter(is_featured=True)[:4],
                "new_products": products.filter(is_new=True)[:4],
                "fox_pick_products": products.filter(is_fox_pick=True, variants__stock_quantity__gt=0).distinct().order_by("-updated_at", "name")[:6],
                "home_moods": MoodCollection.objects.filter(is_active=True)[:7],
                "homepage_story_blocks": get_active_story_blocks(),
                "mood_shopping_enabled": is_feature_enabled("mood_shopping_enabled", True),
                "limited_drops_enabled": is_feature_enabled("limited_drops_enabled", True),
                "page_title": "Airish Fox — мягкая мода с лисьим характером",
                "meta_description": "Airish Fox: boutique fashion, mood-подборки, новинки и fox picks.",
            }
        )
        return context


def healthcheck(request):
    """Return a minimal health status for orchestration checks."""
    return JsonResponse({"status": "ok", "service": "airish-fox"})


def robots_txt(request):
    """Return production-safe crawl rules and expose sitemap.xml."""
    admin_path = f"/{settings.ADMIN_URL}"
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Disallow: {admin_path}",
        "Disallow: /account/",
        "Disallow: /accounts/",
        "Disallow: /cart/",
        "Disallow: /checkout/",
        "Disallow: /payments/",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
