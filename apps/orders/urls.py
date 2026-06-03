"""Order URL routes."""

from django.urls import path

from .views import OrderDetailView, OrderHistoryView

app_name = "orders"

urlpatterns = [
    path("orders/<str:number>/", OrderDetailView.as_view(), name="detail"),
    path("account/orders/", OrderHistoryView.as_view(), name="history"),
]
