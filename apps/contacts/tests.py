from django.test import TestCase
from django.urls import reverse

from .models import ContactRequest


class ContactFormTests(TestCase):
    def test_contacts_page_returns_200(self):
        response = self.client.get(reverse('contacts:contacts'))
        self.assertEqual(response.status_code, 200)

    def test_contact_form_saves_request(self):
        response = self.client.post(reverse('contacts:contacts'), {
            'name': 'Ирина',
            'phone': '+79990000000',
            'email': '',
            'preferred_contact_method': 'telegram',
            'message': 'Хочу образ Airish Fox',
            'source_page': '/contacts/',
            'website': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactRequest.objects.count(), 1)

    def test_honeypot_does_not_save_request(self):
        response = self.client.post(reverse('contacts:contacts'), {
            'name': 'Spam',
            'phone': '+79990000000',
            'preferred_contact_method': 'telegram',
            'message': 'spam',
            'website': 'bot-filled',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactRequest.objects.count(), 0)
