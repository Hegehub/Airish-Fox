"""Catalog models for Airish Fox products, variants and mood collections."""

from decimal import Decimal

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse

from .services import validate_image_extension, validate_image_size

catalog_image_validators = [validate_image_extension, validate_image_size]
color_hex_validator = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message="Цвет должен быть HEX-значением в формате #B8F2D0.",
)


class Category(models.Model):
    name = models.CharField("Название", max_length=120)
    slug = models.SlugField("Slug", unique=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField(
        "Изображение",
        upload_to="catalog/categories/",
        blank=True,
        null=True,
        validators=catalog_image_validators,
    )
    is_active = models.BooleanField("Активна", default=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    seo_title = models.CharField("SEO title", max_length=255, blank=True)
    seo_description = models.TextField("SEO description", blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('catalog:product_list')}?category={self.slug}"


class Collection(models.Model):
    name = models.CharField("Название", max_length=120)
    slug = models.SlugField("Slug", unique=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField(
        "Изображение",
        upload_to="catalog/collections/",
        blank=True,
        null=True,
        validators=catalog_image_validators,
    )
    is_active = models.BooleanField("Активна", default=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    seo_title = models.CharField("SEO title", max_length=255, blank=True)
    seo_description = models.TextField("SEO description", blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:collection_detail", kwargs={"slug": self.slug})


class MoodCollection(models.Model):
    name = models.CharField("Название", max_length=120)
    slug = models.SlugField("Slug", unique=True)
    description = models.TextField("Описание", blank=True)
    color_hex = models.CharField("Цвет", max_length=7, blank=True, default="#B8F2D0", validators=[color_hex_validator])
    image = models.ImageField(
        "Изображение",
        upload_to="catalog/moods/",
        blank=True,
        null=True,
        validators=catalog_image_validators,
    )
    is_active = models.BooleanField("Активна", default=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    seo_title = models.CharField("SEO title", max_length=255, blank=True)
    seo_description = models.TextField("SEO description", blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        verbose_name = "Mood-подборка"
        verbose_name_plural = "Mood-подборки"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:mood_detail", kwargs={"slug": self.slug})


class Product(models.Model):
    name = models.CharField("Название", max_length=160)
    slug = models.SlugField("Slug", unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="Категория")
    collections = models.ManyToManyField(Collection, blank=True, related_name="products", verbose_name="Коллекции")
    moods = models.ManyToManyField(MoodCollection, blank=True, related_name="products", verbose_name="Mood-подборки")
    short_description = models.CharField("Короткое описание", max_length=255)
    description = models.TextField("Описание", blank=True)
    material = models.CharField("Материал", max_length=180, blank=True)
    care_instructions = models.TextField("Уход", blank=True)
    badge = models.CharField("Бейдж", max_length=80, blank=True)
    is_active = models.BooleanField("Активен", default=True)
    is_featured = models.BooleanField("Featured", default=False)
    is_new = models.BooleanField("Новинка", default=False)
    is_fox_pick = models.BooleanField("Fox pick", default=False)
    is_gift_ready = models.BooleanField("Gift ready", default=False)
    seo_title = models.CharField("SEO title", max_length=255, blank=True)
    seo_description = models.TextField("SEO description", blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-is_new", "-is_featured", "name"]
        indexes = [
            models.Index(fields=["is_active"], name="catalog_product_active_idx"),
            models.Index(fields=["is_new"], name="catalog_product_new_idx"),
            models.Index(fields=["is_featured"], name="catalog_product_featured_idx"),
            models.Index(fields=["is_fox_pick"], name="catalog_product_fox_pick_idx"),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})

    def get_main_image(self):
        return self.images.order_by("sort_order", "id").first()

    def get_min_price(self):
        variant = self.get_active_variants().order_by("price").first()
        return variant.price if variant else None

    def get_active_variants(self):
        return self.variants.filter(is_active=True)

    def is_available(self):
        return self.get_active_variants().filter(stock_quantity__gt=0).exists()


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants", verbose_name="Товар")
    sku = models.CharField("SKU", max_length=80, unique=True)
    size = models.CharField("Размер", max_length=40)
    color_name = models.CharField("Цвет", max_length=80)
    color_hex = models.CharField("HEX цвета", max_length=7, default="#B8F2D0", validators=[color_hex_validator])
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    compare_at_price = models.DecimalField(
        "Цена до скидки",
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0"))],
    )
    stock_quantity = models.PositiveIntegerField("Остаток", default=0)
    is_active = models.BooleanField("Активен", default=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Вариант товара"
        verbose_name_plural = "Варианты товара"
        ordering = ["sort_order", "size", "color_name"]
        constraints = [
            models.CheckConstraint(condition=Q(price__gte=0), name="catalog_variant_price_gte_0"),
            models.CheckConstraint(condition=Q(stock_quantity__gte=0), name="catalog_variant_stock_gte_0"),
        ]
        indexes = [models.Index(fields=["is_active"], name="catalog_variant_active_idx")]

    def __str__(self):
        return self.get_display_name()

    def is_in_stock(self):
        return self.is_active and self.stock_quantity > 0

    def can_purchase(self, quantity=1):
        return self.is_in_stock() and self.stock_quantity >= quantity

    def get_display_name(self):
        return f"{self.product.name} — {self.size}, {self.color_name} ({self.sku})"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="Товар")
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Вариант",
        blank=True,
        null=True,
    )
    image = models.ImageField("Изображение", upload_to="catalog/products/", validators=catalog_image_validators)
    alt_text = models.CharField("Alt text", max_length=180, blank=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.alt_text or f"Изображение товара {self.product.name}"
