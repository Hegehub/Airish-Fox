"""Store locator URLs."""

from django.urls import path

from .views import StoreDetailView, StoreListView

app_name = "store_locator"

urlpatterns = [
    path("", StoreListView.as_view(), name="store_list"),
    path("<slug:slug>/", StoreDetailView.as_view(), name="store_detail"),
]
