from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import DropWaitlistEntry, ProductDrop
class DropsTests(TestCase):
    def setUp(self):
        self.drop=ProductDrop.objects.create(name="Mint Drop", slug="mint-drop", starts_at=timezone.now()-timedelta(days=1), ends_at=timezone.now()+timedelta(days=1))
    def test_drops_list_works(self): self.assertEqual(self.client.get(reverse("drops:list")).status_code, 200)
    def test_drop_detail_works(self): self.assertEqual(self.client.get(self.drop.get_absolute_url()).status_code, 200)
    def test_waitlist_saves_entry(self):
        self.client.post(reverse("drops:waitlist", args=[self.drop.slug]), {"email":"a@example.com"})
        self.assertEqual(DropWaitlistEntry.objects.count(), 1)
    def test_duplicate_waitlist_blocked(self):
        url=reverse("drops:waitlist", args=[self.drop.slug])
        self.client.post(url, {"email":"a@example.com"}); self.client.post(url, {"email":"a@example.com"})
        self.assertEqual(DropWaitlistEntry.objects.count(), 1)
