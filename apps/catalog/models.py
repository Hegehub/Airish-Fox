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


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', on_delete=models.PROTECT)
    name = models.CharField('Название', max_length=160)
    slug = models.SlugField('Slug', max_length=180, unique=True)
    short_description = models.CharField('Краткое описание', max_length=240)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    sizes = models.CharField('Размеры', max_length=120, help_text='Например: XS, S, M, L')
    color_name = models.CharField('Название цвета', max_length=80)
    color_hex = models.CharField('HEX цвета', max_length=7, default='#B8F2D0')
    main_image = models.ImageField('Главное изображение', upload_to='products/', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    is_featured = models.BooleanField('Популярный', default=False)
    is_new = models.BooleanField('Новинка', default=False)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-is_new', '-created_at', 'name']

    def __str__(self):
        return self.name


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
