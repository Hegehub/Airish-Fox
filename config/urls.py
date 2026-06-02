"""Root URL configuration for Airish Fox."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.core.sitemaps import sitemaps

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("", include("apps.orders.urls")),
    path("account/", include("apps.accounts.urls")),
    path("cart/", include("apps.cart.urls")),
    path("checkout/", include("apps.checkout.urls")),
    path("payments/", include("apps.payments.urls")),
    path("store/", include("apps.store_locator.urls")),
    path("style-quiz/", include("apps.style_quiz.urls")),
    path("wishlist/", include("apps.wishlist.urls")),
    path("drops/", include("apps.drops.urls")),
    path("", include("apps.catalog.urls")),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
