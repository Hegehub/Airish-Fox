from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from apps.catalog.models import Product

from .forms import ContactRequestForm


def get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def is_rate_limited(request):
    timeout = getattr(settings, 'CONTACT_RATE_LIMIT_SECONDS', 30)
    if timeout <= 0:
        return False
    key = f'airish_fox.contact_rate.{get_client_ip(request) or "unknown"}'
    if cache.get(key):
        return True
    cache.set(key, True, timeout=timeout)
    return False


class ContactsView(FormView):
    template_name = 'pages/contacts.html'
    form_class = ContactRequestForm

    def dispatch(self, request, *args, **kwargs):
        self.product = None
        product_slug = request.GET.get('product') or request.POST.get('product')
        if product_slug:
            self.product = Product.objects.filter(slug=product_slug, is_active=True).first()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('contacts:contacts')

    def form_valid(self, form):
        if form.is_honeypot_filled:
            messages.success(self.request, 'Спасибо! Заявка сохранена — мы скоро свяжемся с вами.')
            return redirect(self.get_success_url())
        if is_rate_limited(self.request):
            messages.success(self.request, 'Спасибо! Мы уже получили вашу заявку и скоро ответим.')
            return redirect(self.get_success_url())
        contact_request = form.save(commit=False)
        contact_request.product = self.product
        contact_request.source_page = self.request.build_absolute_uri(self.request.POST.get('source_page') or self.request.path)
        contact_request.user_agent = self.request.META.get('HTTP_USER_AGENT', '')[:1000]
        contact_request.ip_address = get_client_ip(self.request)
        contact_request.save()
        messages.success(self.request, 'Спасибо! Заявка сохранена — мы скоро свяжемся с вами.')
        return redirect(self.get_success_url())

    def get_initial(self):
        initial = super().get_initial()
        if self.product:
            initial['message'] = f'Здравствуйте! Хочу заказать: {self.product.name}. Цвет: {self.product.color_name}. Размеры: {self.product.sizes}.'
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Контакты Airish Fox',
            'meta_description': 'Свяжитесь с Airish Fox через Telegram, WhatsApp, Instagram, email или форму заявки.',
            'canonical_path': self.request.path,
            'selected_product': self.product,
        })
        return context


def quick_contact(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid() and not form.is_honeypot_filled and not is_rate_limited(request):
            contact_request = form.save(commit=False)
            slug = request.POST.get('product')
            if slug:
                contact_request.product = Product.objects.filter(slug=slug, is_active=True).first()
            contact_request.source_page = request.build_absolute_uri(request.POST.get('source_page') or request.path)
            contact_request.user_agent = request.META.get('HTTP_USER_AGENT', '')[:1000]
            contact_request.ip_address = get_client_ip(request)
            contact_request.save()
        messages.success(request, 'Спасибо! Заявка отправлена.')
    return redirect(request.POST.get('next') or reverse('contacts:contacts'))
