"""Offline Airish Fox store location models."""

from decimal import Decimal
from urllib.parse import quote_plus

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.catalog.services import validate_image_extension, validate_image_size

store_image_validators = [validate_image_extension, validate_image_size]


class StoreLocation(models.Model):
    name = models.CharField("Название", max_length=160)
    slug = models.SlugField("Slug", unique=True)
    short_description = models.CharField("Короткое описание", max_length=255, blank=True)
    description = models.TextField("Описание", blank=True)

    country = models.CharField("Страна", max_length=80, default="Vietnam")
    city = models.CharField("Город", max_length=120)
    district = models.CharField("Район", max_length=120, blank=True)
    street_address = models.CharField("Улица и дом", max_length=255)
    full_address = models.TextField("Полный адрес", blank=True)

    latitude = models.DecimalField("Широта", max_digits=10, decimal_places=7, validators=[MinValueValidator(Decimal("-90")), MaxValueValidator(Decimal("90"))])
    longitude = models.DecimalField("Долгота", max_digits=10, decimal_places=7, validators=[MinValueValidator(Decimal("-180")), MaxValueValidator(Decimal("180"))])

    phone = models.CharField("Телефон", max_length=40, blank=True)
    email = models.EmailField("Email", blank=True)
    whatsapp_url = models.URLField("WhatsApp", blank=True)
    telegram_url = models.URLField("Telegram", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)

    google_maps_place_url = models.URLField("Google Maps place URL", blank=True)
    google_maps_embed_url = models.URLField("Google Maps embed URL", blank=True)

    is_active = models.BooleanField("Активен", default=True)
    is_main_store = models.BooleanField("Главный магазин", default=False)
    pickup_available = models.BooleanField("Самовывоз доступен", default=True)
    fitting_available = models.BooleanField("Примерка доступна", default=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)

    image = models.ImageField("Изображение", upload_to="stores/", blank=True, null=True, validators=store_image_validators)

    seo_title = models.CharField("SEO title", max_length=255, blank=True)
    seo_description = models.TextField("SEO description", blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store_locator:store_detail", kwargs={"slug": self.slug})

    def get_display_address(self):
        if self.full_address:
            return self.full_address
        return ", ".join(part for part in [self.street_address, self.district, self.city, self.country] if part)

    def get_directions_url(self):
        if self.latitude is not None and self.longitude is not None:
            return f"https://www.google.com/maps/dir/?api=1&destination={self.latitude},{self.longitude}"
        return f"https://www.google.com/maps/dir/?api=1&destination={quote_plus(self.get_display_address())}"


class StoreOpeningHour(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    WEEKDAY_NAMES_RU = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье",
    }

    store = models.ForeignKey(StoreLocation, related_name="opening_hours", on_delete=models.CASCADE, verbose_name="Магазин")
    weekday = models.PositiveSmallIntegerField("День недели", choices=Weekday.choices)
    opens_at = models.TimeField("Открывается", null=True, blank=True)
    closes_at = models.TimeField("Закрывается", null=True, blank=True)
    is_closed = models.BooleanField("Закрыто", default=False)
    note = models.CharField("Заметка", max_length=160, blank=True)

    class Meta:
        verbose_name = "Часы работы"
        verbose_name_plural = "Часы работы"
        ordering = ["weekday"]
        unique_together = ["store", "weekday"]

    def __str__(self):
        return f"{self.store}: {self.get_weekday_display_name()}"

    def get_weekday_display_name(self):
        return self.WEEKDAY_NAMES_RU.get(self.weekday, self.get_weekday_display())

    def is_open_today(self):
        return self.weekday == timezone.localdate().weekday() and not self.is_closed


class StorePhoto(models.Model):
    store = models.ForeignKey(StoreLocation, related_name="photos", on_delete=models.CASCADE, verbose_name="Магазин")
    image = models.ImageField("Фото", upload_to="stores/gallery/", validators=store_image_validators)
    alt_text = models.CharField("Alt text", max_length=180, blank=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Фото магазина"
        verbose_name_plural = "Фото магазина"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.alt_text or f"Фото {self.store}"
