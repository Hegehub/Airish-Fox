from django.http import HttpResponse
from django.views.generic import TemplateView

from apps.catalog.models import Category, MoodCollection, Product
from apps.contacts.forms import ContactRequestForm
from apps.reviews.models import Review


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Airish Fox — брендовая витрина одежды',
            'meta_description': 'Airish Fox — нежная fashion-витрина одежды с новинками, mood-подборками и быстрым заказом.',
            'canonical_path': self.request.path,
            'categories': Category.objects.filter(is_active=True)[:4],
            'moods': MoodCollection.objects.filter(is_active=True)[:6],
            'featured_products': Product.objects.filter(is_active=True, available=True, is_featured=True).select_related('category').prefetch_related('moods')[:6],
            'new_products': Product.objects.filter(is_active=True, available=True, is_new=True).select_related('category').prefetch_related('moods')[:6],
            'fox_pick_products': Product.objects.filter(is_active=True, available=True, is_fox_pick=True).select_related('category').prefetch_related('moods').order_by('sort_order', '-updated_at')[:6],
            'daily_pick': Product.objects.filter(is_active=True, available=True, is_daily_pick=True).select_related('category').prefetch_related('moods').first(),
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
            'canonical_path': self.request.path,
        })
        return context


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        f'Sitemap: {request.build_absolute_uri("/sitemap.xml")}',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')
