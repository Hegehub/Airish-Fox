from apps.catalog.models import Product
from .models import Wishlist, WishlistItem

def _ensure_session(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key

def get_or_create_wishlist(request):
    if request.user.is_authenticated:
        return Wishlist.objects.get_or_create(user=request.user, session_key="")[0]
    return Wishlist.objects.get_or_create(session_key=_ensure_session(request), user=None)[0]

def get_existing_wishlist(request):
    if request.user.is_authenticated:
        return Wishlist.objects.filter(user=request.user).first()
    key = request.session.session_key
    return Wishlist.objects.filter(session_key=key, user=None).first() if key else None

def add_product(request, product_id):
    product = Product.objects.get(pk=product_id, is_active=True)
    wishlist = get_or_create_wishlist(request)
    WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    return wishlist

def remove_product(request, product_id):
    wishlist = get_existing_wishlist(request)
    if wishlist:
        wishlist.items.filter(product_id=product_id).delete()
    return wishlist

def merge_session_wishlist_into_user(request, user):
    key = request.session.session_key
    if not key:
        return None
    session_wishlist = Wishlist.objects.filter(session_key=key, user=None).first()
    if not session_wishlist:
        return None
    user_wishlist = Wishlist.objects.get_or_create(user=user, session_key="")[0]
    for item in session_wishlist.items.all():
        WishlistItem.objects.get_or_create(wishlist=user_wishlist, product=item.product)
    session_wishlist.delete()
    return user_wishlist
