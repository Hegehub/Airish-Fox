from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import FormView

from .forms import ContactRequestForm


class ContactsView(FormView):
    template_name = 'pages/contacts.html'
    form_class = ContactRequestForm

    def get_success_url(self):
        return reverse('contacts:contacts')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Спасибо! Заявка сохранена — мы скоро свяжемся с вами.')
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Контакты Airish Fox',
            'meta_description': 'Свяжитесь с Airish Fox через Telegram, WhatsApp, Instagram, email или форму заявки.',
        })
        return context


def quick_contact(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо! Заявка отправлена.')
    return redirect(request.POST.get('next') or reverse('contacts:contacts'))
