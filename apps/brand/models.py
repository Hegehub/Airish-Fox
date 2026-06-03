"""Admin-managed brand experience primitives."""
from django.core.validators import RegexValidator
from django.db import models

from apps.catalog.services import validate_image_extension, validate_image_size

color_hex_validator = RegexValidator(r"^#[0-9A-Fa-f]{6}$", "Укажите HEX цвет в формате #B8F2D0.")
image_validators = [validate_image_extension, validate_image_size]

class BrandFeatureToggle(models.Model):
    key = models.SlugField("Key", unique=True)
    name = models.CharField("Название", max_length=140)
    description = models.TextField("Описание", blank=True)
    is_enabled = models.BooleanField("Включено", default=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    class Meta:
        verbose_name = "Brand feature toggle"
        verbose_name_plural = "Brand feature toggles"
        ordering = ["key"]
    def __str__(self): return self.name

class HomepageStoryBlock(models.Model):
    title = models.CharField("Заголовок", max_length=160)
    subtitle = models.CharField("Подзаголовок", max_length=180, blank=True)
    text = models.TextField("Текст", blank=True)
    image = models.ImageField("Изображение", upload_to="brand/story/", blank=True, null=True, validators=image_validators)
    mascot_state = models.CharField("Mascot state", max_length=40, blank=True, default="happy")
    cta_label = models.CharField("CTA label", max_length=80, blank=True)
    cta_url = models.CharField("CTA URL", max_length=240, blank=True)
    is_active = models.BooleanField("Активен", default=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    class Meta:
        verbose_name = "Homepage story block"
        verbose_name_plural = "Homepage story blocks"
        ordering = ["sort_order", "title"]
    def __str__(self): return self.title

class BrandBadge(models.Model):
    name = models.CharField("Название", max_length=120)
    slug = models.SlugField("Slug", unique=True)
    label = models.CharField("Label", max_length=80)
    description = models.TextField("Описание", blank=True)
    color_hex = models.CharField("Цвет", max_length=7, default="#B8F2D0", validators=[color_hex_validator])
    icon_svg_name = models.CharField("SVG icon name", max_length=80, blank=True)
    is_active = models.BooleanField("Активен", default=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    class Meta:
        verbose_name = "Brand badge"
        verbose_name_plural = "Brand badges"
        ordering = ["sort_order", "name"]
    def __str__(self): return self.label or self.name
