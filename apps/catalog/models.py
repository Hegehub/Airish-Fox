from urllib.parse import urlencode

from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Название', max_length=120)
    slug = models.SlugField('Slug', max_length=140, unique=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='categories/', blank=True)
    is_active = models.BooleanField('Активна', default=True)
    sort_order = models.PositiveIntegerField('Порядок сортировки', default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'{reverse("catalog:collection")}?category={self.slug}'


class MoodCollection(models.Model):
    name = models.CharField('Название', max_length=120)
    slug = models.SlugField('Slug', max_length=140, unique=True)
    description = models.TextField('Описание', blank=True)
    color_hex = models.CharField('HEX акцент', max_length=7, default='#B8F2D0')
    image = models.ImageField('Изображение', upload_to='moods/', blank=True)
    is_active = models.BooleanField('Активна', default=True)
    sort_order = models.PositiveIntegerField('Порядок сортировки', default=0)

    class Meta:
        verbose_name = 'Mood-подборка'
        verbose_name_plural = 'Mood-подборки'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'{reverse("catalog:collection")}?mood={self.slug}'


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', on_delete=models.PROTECT)
    moods = models.ManyToManyField(MoodCollection, verbose_name='Mood-подборки', blank=True, related_name='products')
    name = models.CharField('Название', max_length=160)
    slug = models.SlugField('Slug', max_length=180, unique=True)
    short_description = models.CharField('Краткое описание', max_length=240)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    sizes = models.CharField('Размеры', max_length=120, help_text='Например: XS, S, M, L')
    color_name = models.CharField('Название цвета', max_length=80)
    color_hex = models.CharField('HEX цвета', max_length=7, default='#B8F2D0')
    main_image = models.ImageField('Главное изображение', upload_to='products/', blank=True)
    badge = models.CharField('Бейдж', max_length=80, blank=True)
    whatsapp_message = models.TextField('Сообщение WhatsApp', blank=True)
    telegram_message = models.TextField('Сообщение Telegram', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    available = models.BooleanField('Доступен', default=True)
    is_featured = models.BooleanField('Популярный', default=False)
    is_new = models.BooleanField('Новинка', default=False)
    is_fox_pick = models.BooleanField('Лисичка советует', default=False)
    is_gift_ready = models.BooleanField('Готово для подарка', default=False)
    is_daily_pick = models.BooleanField('Образ дня', default=False)
    sort_order = models.PositiveIntegerField('Порядок сортировки', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['sort_order', '-is_new', '-updated_at', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    def get_order_message(self, request=None, channel: str = '') -> str:
        if channel == 'whatsapp' and self.whatsapp_message:
            return self.whatsapp_message
        if channel == 'telegram' and self.telegram_message:
            return self.telegram_message
        product_url = self.get_absolute_url()
        if request is not None:
            product_url = request.build_absolute_uri(product_url)
        return (
            f'Здравствуйте! Хочу заказать: {self.name}.\n'
            f'Цвет: {self.color_name}.\n'
            f'Размеры: {self.sizes}.\n'
            f'Ссылка: {product_url}'
        )

    def get_whatsapp_order_url(self, site_settings=None, request=None):
        base_url = getattr(site_settings, 'whatsapp_url', '') if site_settings else ''
        if not base_url:
            return f'{reverse("contacts:contacts")}?{urlencode({"product": self.slug})}'
        separator = '&' if '?' in base_url else '?'
        return f'{base_url}{separator}{urlencode({"text": self.get_order_message(request=request, channel="whatsapp")})}'

    def get_telegram_order_url(self, site_settings=None, request=None):
        base_url = getattr(site_settings, 'telegram_url', '') if site_settings else ''
        if not base_url:
            return f'{reverse("contacts:contacts")}?{urlencode({"product": self.slug})}'
        separator = '&' if '?' in base_url else '?'
        return f'{base_url}{separator}{urlencode({"text": self.get_order_message(request=request, channel="telegram")})}'

    def get_primary_order_url(self, site_settings=None, request=None):
        method = getattr(site_settings, 'primary_contact_method', 'telegram') if site_settings else 'telegram'
        if method == 'whatsapp':
            return self.get_whatsapp_order_url(site_settings=site_settings, request=request)
        if method == 'telegram':
            return self.get_telegram_order_url(site_settings=site_settings, request=request)
        return f'{reverse("contacts:contacts")}?{urlencode({"product": self.slug})}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Изображение', upload_to='products/gallery/')
    alt_text = models.CharField('Alt-текст', max_length=180, blank=True)
    sort_order = models.PositiveIntegerField('Порядок сортировки', default=0)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.alt_text or f'Изображение {self.product.name}'
