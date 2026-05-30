from django.urls import path

from .views import CollectionView, NewArrivalsView, ProductDetailView

app_name = 'catalog'

urlpatterns = [
    path('', CollectionView.as_view(), name='collection'),
    path('new/', NewArrivalsView.as_view(), name='new_arrivals'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
