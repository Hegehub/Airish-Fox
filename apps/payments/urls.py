"""Payment URL routes."""

from django.urls import path

from .views import AntomCreatePaymentView, AntomNotifyView, AntomReturnView

app_name = "payments"

urlpatterns = [
    path("antom/create/<str:order_number>/", AntomCreatePaymentView.as_view(), name="antom_create"),
    path("antom/return/", AntomReturnView.as_view(), name="antom_return"),
    path("antom/notify/", AntomNotifyView.as_view(), name="antom_notify"),
]
