from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from apps.catalog.services import validate_image_extension, validate_image_size

class ProductDrop(models.Model):
    name = models.CharField("Название", max_length=160)
    slug = models.SlugField("Slug", unique=True)
    description = models.TextField("Описание", blank=True)
    hero_image = models.ImageField("Hero image", upload_to="drops/", blank=True, null=True, validators=[validate_image_extension, validate_image_size])
    products = models.ManyToManyField("catalog.Product", blank=True, related_name="drops")
    starts_at = models.DateTimeField("Начало")
    ends_at = models.DateTimeField("Окончание")
    is_active = models.BooleanField("Активен", default=True)
    show_countdown = models.BooleanField("Показывать countdown", default=True)
    waitlist_enabled = models.BooleanField("Waitlist", default=True)
    seo_title = models.CharField("SEO title", max_length=255, blank=True)
    seo_description = models.TextField("SEO description", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Product drop"
        verbose_name_plural = "Product drops"
        ordering = ["-starts_at", "name"]
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse("drops:detail", kwargs={"slug": self.slug})
    def is_visible(self):
        now = timezone.now()
        return self.is_active and self.ends_at >= now
    def is_live(self):
        now = timezone.now()
        return self.is_active and self.starts_at <= now <= self.ends_at

class DropWaitlistEntry(models.Model):
    drop = models.ForeignKey(ProductDrop, related_name="waitlist_entries", on_delete=models.CASCADE)
    email = models.EmailField("Email")
    name = models.CharField("Имя", max_length=120, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="drop_waitlist_entries")
    created_at = models.DateTimeField(auto_now_add=True)
    is_notified = models.BooleanField("Уведомлён", default=False)
    class Meta:
        verbose_name = "Drop waitlist entry"
        verbose_name_plural = "Drop waitlist entries"
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["drop", "email"], name="drops_unique_waitlist_email")]
    def __str__(self): return self.email
