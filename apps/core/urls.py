from django.urls import path

from .views import AboutView, HomeView, robots_txt

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('robots.txt', robots_txt, name='robots_txt'),
]
