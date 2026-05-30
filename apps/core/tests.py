from django.test import TestCase
from django.urls import reverse


class CorePageTests(TestCase):
    def test_home_page_returns_200(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_robots_txt_returns_200(self):
        response = self.client.get(reverse('core:robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sitemap:')
