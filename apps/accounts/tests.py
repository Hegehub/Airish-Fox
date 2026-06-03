"""Tests for customer accounts, profiles and addresses."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Address, CustomerProfile


class AccountsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="airish", email="airish@example.com", password="StrongPass123")
        self.other_user = User.objects.create_user(username="other", email="other@example.com", password="StrongPass123")

    def registration_data(self, **overrides):
        data = {
            "username": "newfox",
            "email": "newfox@example.com",
            "password1": "VeryStrongPass123",
            "password2": "VeryStrongPass123",
        }
        data.update(overrides)
        return data

    def address_data(self, **overrides):
        data = {
            "full_name": "Airish Fox",
            "phone": "+84900000000",
            "country": "Vietnam",
            "city": "Ho Chi Minh City",
            "district": "District 1",
            "ward": "Ben Nghe",
            "street_address": "1 Boutique Street",
            "postal_code": "700000",
            "delivery_notes": "Call before delivery",
            "is_default_shipping": "on",
        }
        data.update(overrides)
        return data

    def test_register_page_returns_200(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_register(self):
        response = self.client.post(reverse("accounts:register"), self.registration_data(), follow=True)
        self.assertRedirects(response, reverse("accounts:dashboard"))
        self.assertTrue(User.objects.filter(username="newfox", email="newfox@example.com").exists())
        self.assertTrue(response.context["user"].is_authenticated)

    def test_customer_profile_auto_created(self):
        user = User.objects.create_user(username="profiled", email="profiled@example.com", password="StrongPass123")
        self.assertTrue(CustomerProfile.objects.filter(user=user).exists())

    def test_email_required_on_registration(self):
        response = self.client.post(reverse("accounts:register"), self.registration_data(email=""))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newfox").exists())
        self.assertFormError(response.context["form"], "email", "Обязательное поле.")

    def test_duplicate_email_rejected(self):
        response = self.client.post(reverse("accounts:register"), self.registration_data(email="airish@example.com"))
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "email", "Пользователь с таким email уже существует.")

    def test_login_page_returns_200(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])

    def test_authenticated_user_can_access_dashboard(self):
        self.client.login(username="airish", password="StrongPass123")
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Личный кабинет")

    def test_user_can_update_profile(self):
        self.client.login(username="airish", password="StrongPass123")
        response = self.client.post(
            reverse("accounts:profile"),
            {
                "phone": "+84911111111",
                "birthday": "1995-05-10",
                "preferred_size_top": "M",
                "preferred_size_bottom": "S",
                "preferred_fit": "regular",
                "favorite_color": "Mint",
                "favorite_mood": "",
                "marketing_consent": "on",
            },
        )
        self.assertRedirects(response, reverse("accounts:dashboard"))
        self.user.customer_profile.refresh_from_db()
        self.assertEqual(self.user.customer_profile.phone, "+84911111111")
        self.assertEqual(self.user.customer_profile.preferred_fit, "regular")
        self.assertTrue(self.user.customer_profile.marketing_consent)

    def test_user_can_create_address(self):
        self.client.login(username="airish", password="StrongPass123")
        response = self.client.post(reverse("accounts:address_create"), self.address_data())
        self.assertRedirects(response, reverse("accounts:address_list"))
        self.assertTrue(self.user.addresses.filter(city="Ho Chi Minh City").exists())

    def test_user_can_set_default_shipping_address(self):
        self.client.login(username="airish", password="StrongPass123")
        self.client.post(reverse("accounts:address_create"), self.address_data())
        address = self.user.addresses.get()
        self.assertTrue(address.is_default_shipping)

    def test_only_one_default_shipping_address_per_user(self):
        first = Address.objects.create(user=self.user, full_name="First", phone="1", city="HCMC", street_address="One", is_default_shipping=True)
        second = Address.objects.create(user=self.user, full_name="Second", phone="2", city="HCMC", street_address="Two", is_default_shipping=True)
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertFalse(first.is_default_shipping)
        self.assertTrue(second.is_default_shipping)
        self.assertEqual(self.user.addresses.filter(is_default_shipping=True).count(), 1)

    def test_user_cannot_edit_another_users_address(self):
        other_address = Address.objects.create(user=self.other_user, full_name="Other", phone="1", city="Hanoi", street_address="Other")
        self.client.login(username="airish", password="StrongPass123")
        response = self.client.post(reverse("accounts:address_update", kwargs={"pk": other_address.pk}), self.address_data(city="Hacked"))
        self.assertEqual(response.status_code, 404)
        other_address.refresh_from_db()
        self.assertEqual(other_address.city, "Hanoi")

    def test_user_cannot_delete_another_users_address(self):
        other_address = Address.objects.create(user=self.other_user, full_name="Other", phone="1", city="Hanoi", street_address="Other")
        self.client.login(username="airish", password="StrongPass123")
        response = self.client.post(reverse("accounts:address_delete", kwargs={"pk": other_address.pk}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Address.objects.filter(pk=other_address.pk).exists())

    def test_address_list_shows_only_current_users_addresses(self):
        own_address = Address.objects.create(user=self.user, full_name="Own", phone="1", city="HCMC", street_address="Own")
        Address.objects.create(user=self.other_user, full_name="Other", phone="2", city="Hanoi", street_address="Other")
        self.client.login(username="airish", password="StrongPass123")
        response = self.client.get(reverse("accounts:address_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, own_address.full_name)
        self.assertNotContains(response, "Other")
