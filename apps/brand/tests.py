from django.test import TestCase
from django.urls import reverse
from apps.brand.models import HomepageStoryBlock

class BrandHomeTests(TestCase):
    def test_active_story_blocks_render_on_home(self):
        HomepageStoryBlock.objects.create(title="Мягкая мята", text="История бренда", is_active=True)
        HomepageStoryBlock.objects.create(title="Hidden", is_active=False)
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Мягкая мята")
        self.assertNotContains(response, "Hidden")
