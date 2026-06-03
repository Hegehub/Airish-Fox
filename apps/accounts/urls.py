"""Account URL routes."""

from django.urls import path

from .views import (
    AddressCreateView,
    AddressDeleteView,
    AddressListView,
    AddressUpdateView,
    DashboardView,
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    ProfileUpdateView,
    RegisterView,
)

app_name = "accounts"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    path("password/", PasswordChangeView.as_view(), name="password_change"),
    path("password/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("addresses/", AddressListView.as_view(), name="address_list"),
    path("addresses/new/", AddressCreateView.as_view(), name="address_create"),
    path("addresses/<int:pk>/edit/", AddressUpdateView.as_view(), name="address_update"),
    path("addresses/<int:pk>/delete/", AddressDeleteView.as_view(), name="address_delete"),
]
