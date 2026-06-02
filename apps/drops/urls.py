from django.urls import path
from .views import DropDetailView, DropListView, DropWaitlistView
app_name="drops"
urlpatterns=[path("", DropListView.as_view(), name="list"), path("<slug:slug>/", DropDetailView.as_view(), name="detail"), path("<slug:slug>/waitlist/", DropWaitlistView.as_view(), name="waitlist")]
