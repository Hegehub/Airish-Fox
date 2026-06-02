"""URL routes for core pages."""

from django.urls import path

from .views import HomeView, healthcheck, robots_txt

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("health/", healthcheck, name="healthcheck"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("robots.txt/", robots_txt, name="robots_txt_slash"),
]
