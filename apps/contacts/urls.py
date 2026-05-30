from django.urls import path

from .views import ContactsView, quick_contact

app_name = 'contacts'

urlpatterns = [
    path('', ContactsView.as_view(), name='contacts'),
    path('quick/', quick_contact, name='quick_contact'),
]
