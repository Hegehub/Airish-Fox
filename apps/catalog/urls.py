"""Catalog URL routes."""

from django.urls import path

from .views import CollectionDetailView, CollectionListView, MoodDetailView, NewArrivalsView, ProductDetailView, ProductListView

app_name = "catalog"

urlpatterns = [
    path("catalog/", ProductListView.as_view(), name="product_list"),
    path("catalog/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("new/", NewArrivalsView.as_view(), name="new_arrivals"),
    path("collections/", CollectionListView.as_view(), name="collection_list"),
    path("collections/<slug:slug>/", CollectionDetailView.as_view(), name="collection_detail"),
    path("moods/<slug:slug>/", MoodDetailView.as_view(), name="mood_detail"),
]
