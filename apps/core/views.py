from django.views.generic import TemplateView

from apps.catalog.models import Category, Product
from apps.contacts.forms import ContactRequestForm
from apps.reviews.models import Review


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Airish Fox — брендовая витрина одежды',
            'meta_description': 'Airish Fox — нежная fashion-витрина одежды с новинками, коллекциями и уютными образами.',
            'categories': Category.objects.filter(is_active=True)[:4],
            'featured_products': Product.objects.filter(is_active=True, is_featured=True).select_related('category')[:6],
            'new_products': Product.objects.filter(is_active=True, is_new=True).select_related('category')[:6],
            'reviews': Review.objects.filter(is_active=True)[:3],
            'contact_form': ContactRequestForm(),
        })
        return context


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'О бренде Airish Fox',
            'meta_description': 'Философия Airish Fox: мягкий fashion, индивидуальность, уют и яркие акценты.',
        })
        return context
