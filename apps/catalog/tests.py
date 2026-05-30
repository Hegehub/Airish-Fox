from django.test import TestCase
from django.urls import reverse

from .models import Category, MoodCollection, Product


class CatalogPageTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Платья', slug='dresses', is_active=True)
        self.mood = MoodCollection.objects.create(name='Mint Mood', slug='mint-mood', is_active=True)
        self.product = Product.objects.create(
            category=self.category,
            name='Mint Slip Dress',
            slug='mint-slip-dress',
            short_description='Нежное платье для boutique-настроения.',
            price=7900,
            sizes='XS, S, M',
            color_name='Cat Mint',
            color_hex='#B8F2D0',
            is_active=True,
            available=True,
            is_new=True,
            is_fox_pick=True,
        )
        self.product.moods.add(self.mood)

    def test_collection_page_returns_200(self):
        response = self.client.get(reverse('catalog:collection'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_category_filter_works(self):
        response = self.client.get(reverse('catalog:collection'), {'category': self.category.slug})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_mood_filter_works(self):
        response = self.client.get(reverse('catalog:collection'), {'mood': self.mood.slug})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_new_arrivals_filter_works(self):
        response = self.client.get(reverse('catalog:new_arrivals'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_returns_200(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_fox_pick_products_are_shown_on_home(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
