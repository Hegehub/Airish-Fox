"""Store locator context helpers."""

from .models import StoreLocation


def store_context(request):
    main_store = StoreLocation.objects.filter(is_active=True).only("name", "slug", "city", "district", "street_address", "full_address", "latitude", "longitude", "sort_order", "is_main_store").order_by("-is_main_store", "sort_order", "name").first()
    return {"footer_main_store": main_store}
