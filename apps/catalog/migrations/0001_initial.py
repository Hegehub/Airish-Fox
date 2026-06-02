# Generated manually for Airish Fox catalog stage 2.

import decimal
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import apps.catalog.services


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Название")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("image", models.ImageField(blank=True, null=True, upload_to="catalog/categories/", validators=[apps.catalog.services.validate_image_extension, apps.catalog.services.validate_image_size], verbose_name="Изображение")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активна")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("seo_title", models.CharField(blank=True, max_length=255, verbose_name="SEO title")),
                ("seo_description", models.TextField(blank=True, verbose_name="SEO description")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создана")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлена")),
            ],
            options={"verbose_name": "Категория", "verbose_name_plural": "Категории", "ordering": ["sort_order", "name"]},
        ),
        migrations.CreateModel(
            name="Collection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Название")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("image", models.ImageField(blank=True, null=True, upload_to="catalog/collections/", validators=[apps.catalog.services.validate_image_extension, apps.catalog.services.validate_image_size], verbose_name="Изображение")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активна")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("seo_title", models.CharField(blank=True, max_length=255, verbose_name="SEO title")),
                ("seo_description", models.TextField(blank=True, verbose_name="SEO description")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создана")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлена")),
            ],
            options={"verbose_name": "Коллекция", "verbose_name_plural": "Коллекции", "ordering": ["sort_order", "name"]},
        ),
        migrations.CreateModel(
            name="MoodCollection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Название")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("color_hex", models.CharField(blank=True, default="#B8F2D0", max_length=7, validators=[django.core.validators.RegexValidator(message="Цвет должен быть HEX-значением в формате #B8F2D0.", regex="^#[0-9A-Fa-f]{6}$")], verbose_name="Цвет")),
                ("image", models.ImageField(blank=True, null=True, upload_to="catalog/moods/", validators=[apps.catalog.services.validate_image_extension, apps.catalog.services.validate_image_size], verbose_name="Изображение")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активна")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("seo_title", models.CharField(blank=True, max_length=255, verbose_name="SEO title")),
                ("seo_description", models.TextField(blank=True, verbose_name="SEO description")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создана")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлена")),
            ],
            options={"verbose_name": "Mood-подборка", "verbose_name_plural": "Mood-подборки", "ordering": ["sort_order", "name"]},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160, verbose_name="Название")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                ("short_description", models.CharField(max_length=255, verbose_name="Короткое описание")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("material", models.CharField(blank=True, max_length=180, verbose_name="Материал")),
                ("care_instructions", models.TextField(blank=True, verbose_name="Уход")),
                ("badge", models.CharField(blank=True, max_length=80, verbose_name="Бейдж")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активен")),
                ("is_featured", models.BooleanField(default=False, verbose_name="Featured")),
                ("is_new", models.BooleanField(default=False, verbose_name="Новинка")),
                ("is_fox_pick", models.BooleanField(default=False, verbose_name="Fox pick")),
                ("is_gift_ready", models.BooleanField(default=False, verbose_name="Gift ready")),
                ("seo_title", models.CharField(blank=True, max_length=255, verbose_name="SEO title")),
                ("seo_description", models.TextField(blank=True, verbose_name="SEO description")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="catalog.category", verbose_name="Категория")),
                ("collections", models.ManyToManyField(blank=True, related_name="products", to="catalog.collection", verbose_name="Коллекции")),
                ("moods", models.ManyToManyField(blank=True, related_name="products", to="catalog.moodcollection", verbose_name="Mood-подборки")),
            ],
            options={"verbose_name": "Товар", "verbose_name_plural": "Товары", "ordering": ["-is_new", "-is_featured", "name"]},
        ),
        migrations.CreateModel(
            name="ProductVariant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sku", models.CharField(max_length=80, unique=True, verbose_name="SKU")),
                ("size", models.CharField(max_length=40, verbose_name="Размер")),
                ("color_name", models.CharField(max_length=80, verbose_name="Цвет")),
                ("color_hex", models.CharField(default="#B8F2D0", max_length=7, validators=[django.core.validators.RegexValidator(message="Цвет должен быть HEX-значением в формате #B8F2D0.", regex="^#[0-9A-Fa-f]{6}$")], verbose_name="HEX цвета")),
                ("price", models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Цена")),
                ("compare_at_price", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Цена до скидки")),
                ("stock_quantity", models.PositiveIntegerField(default=0, verbose_name="Остаток")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активен")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="variants", to="catalog.product", verbose_name="Товар")),
            ],
            options={"verbose_name": "Вариант товара", "verbose_name_plural": "Варианты товара", "ordering": ["sort_order", "size", "color_name"]},
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="catalog/products/", validators=[apps.catalog.services.validate_image_extension, apps.catalog.services.validate_image_size], verbose_name="Изображение")),
                ("alt_text", models.CharField(blank=True, max_length=180, verbose_name="Alt text")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="catalog.product", verbose_name="Товар")),
                ("variant", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="images", to="catalog.productvariant", verbose_name="Вариант")),
            ],
            options={"verbose_name": "Изображение товара", "verbose_name_plural": "Изображения товаров", "ordering": ["sort_order", "id"]},
        ),
        migrations.AddConstraint(
            model_name="productvariant",
            constraint=models.CheckConstraint(condition=models.Q(price__gte=0), name="catalog_variant_price_gte_0"),
        ),
        migrations.AddConstraint(
            model_name="productvariant",
            constraint=models.CheckConstraint(condition=models.Q(stock_quantity__gte=0), name="catalog_variant_stock_gte_0"),
        ),
    ]
