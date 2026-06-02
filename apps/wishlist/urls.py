from django.urls import path
from .views import WishlistAddView, WishlistDetailView, WishlistRemoveView, WishlistToggleView
app_name = "wishlist"
urlpatterns = [path("", WishlistDetailView.as_view(), name="detail"), path("add/<int:product_id>/", WishlistAddView.as_view(), name="add"), path("remove/<int:product_id>/", WishlistRemoveView.as_view(), name="remove"), path("toggle/<int:product_id>/", WishlistToggleView.as_view(), name="toggle")]
