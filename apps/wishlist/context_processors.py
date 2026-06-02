from .services import get_existing_wishlist

def wishlist_summary(request):
    wishlist = get_existing_wishlist(request)
    return {"wishlist_items_count": wishlist.get_items_count() if wishlist else 0}
